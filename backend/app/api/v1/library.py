from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Book, UserLibrary
from app.db.session import get_db
from app.schemas.library import LibraryEntryCreate, LibraryEntryRead

router = APIRouter(prefix="/library", tags=["library"])


@router.get("", response_model=list[LibraryEntryRead])
def list_library(db: Session = Depends(get_db)):
    return db.query(UserLibrary).all()


@router.post("", response_model=LibraryEntryRead)
def add_to_library(entry: LibraryEntryCreate, db: Session = Depends(get_db)):
    # Upsert by book_id
    existing = db.query(UserLibrary).filter(UserLibrary.book_id == entry.book_id).first()
    if existing:
        existing.is_liked = entry.is_liked
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    # Ensure book exists
    if not db.get(Book, entry.book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    record = UserLibrary(book_id=entry.book_id, is_liked=entry.is_liked)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.patch("/{book_id}", response_model=LibraryEntryRead)
def toggle_like(book_id: int, db: Session = Depends(get_db)):
    record = db.query(UserLibrary).filter(UserLibrary.book_id == book_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not in library")
    record.is_liked = not record.is_liked
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
