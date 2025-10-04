from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512), index=True)
    author: Mapped[str] = mapped_column(String(512), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    google_books_id: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True)
    cover_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    summaries: Mapped[list["Summary"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    embeddings: Mapped[list["Embedding"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    library_entries: Mapped[list["UserLibrary"]] = relationship(back_populates="book", cascade="all, delete-orphan")


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    content: Mapped[str] = mapped_column(Text)
    tone: Mapped[str] = mapped_column(String(64))
    length: Mapped[str] = mapped_column(String(64))
    audience: Mapped[str] = mapped_column(String(64))
    audio_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    book: Mapped[Book] = relationship(back_populates="summaries")


class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    book: Mapped[Book] = relationship(back_populates="embeddings")


class UserLibrary(Base):
    __tablename__ = "user_library"
    __table_args__ = (
        UniqueConstraint("book_id", name="uq_userlibrary_book"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    is_liked: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    book: Mapped[Book] = relationship(back_populates="library_entries")
