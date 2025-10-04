from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LibraryEntryBase(BaseModel):
    book_id: int
    is_liked: bool = True


class LibraryEntryCreate(LibraryEntryBase):
    pass


class LibraryEntryRead(LibraryEntryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
