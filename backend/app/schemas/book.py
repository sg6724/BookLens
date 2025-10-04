from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    google_books_id: Optional[str] = None
    cover_url: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    created_at: datetime
