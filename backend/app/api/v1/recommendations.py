from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Book
from app.db.session import get_db
from app.schemas.book import BookRead
from app.services.recommender import recommender

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/books/{book_id}", response_model=list[BookRead])
def get_recommendations(book_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    ids = recommender.recommend(db, book_id=book_id, top_k=top_k)
    if not ids:
        return []
    books = db.query(Book).filter(Book.id.in_(ids)).all()
    # Preserve order of ids
    order = {bid: i for i, bid in enumerate(ids)}
    books.sort(key=lambda b: order.get(b.id, 1_000_000))
    return books
