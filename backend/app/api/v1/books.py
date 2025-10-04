from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Book, Summary
from app.db.session import get_db
from app.schemas.book import BookRead
from app.services.books_api import extract_book_metadata, search_google_books
from app.services.files import save_upload
from app.services.ocr import ocr_image
from app.utils.text import pick_likely_title
from app.schemas.summary import SummaryRead

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/identify")
async def identify_book(image: UploadFile = File(...), db: Session = Depends(get_db)):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image upload")

    path = save_upload(await image.read(), image.filename)
    text = ocr_image(path)
    # Basic heuristics
    lines = [ln for ln in text.splitlines() if ln.strip()]
    title = pick_likely_title(lines) or (lines[0] if lines else "")
    query = title or text[:120]

    item = await search_google_books(query)
    if not item:
        # If nothing from Google, create a minimal book record
        book = Book(title=title or "Unknown", author="", description=None, google_books_id=None)
        db.add(book)
        db.commit()
        db.refresh(book)
        return {"book": BookRead.model_validate(book), "ocr_text": text}

    meta = extract_book_metadata(item)
    # Upsert by google_books_id if available
    book = None
    if meta.get("google_books_id"):
        book = db.execute(select(Book).where(Book.google_books_id == meta["google_books_id"])).scalar_one_or_none()
    if not book:
        book = Book(
            title=meta.get("title") or title or "Unknown",
            author=meta.get("author") or "Unknown",
            description=meta.get("description"),
            google_books_id=meta.get("google_books_id"),
            cover_url=meta.get("cover_url"),
        )
        db.add(book)
        db.commit()
        db.refresh(book)
    else:
        # Update missing fields
        updated = False
        for field in ["title", "author", "description", "cover_url"]:
            val = meta.get(field)
            if val and not getattr(book, field):
                setattr(book, field, val)
                updated = True
        if updated:
            db.add(book)
            db.commit()
            db.refresh(book)

    return {"book": BookRead.model_validate(book), "ocr_text": text, "metadata": meta.get("raw")}
