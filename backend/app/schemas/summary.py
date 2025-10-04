from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SummaryBase(BaseModel):
    content: str
    tone: str
    length: str
    audience: str
    audio_path: Optional[str] = None

    model_config = {"from_attributes": True}


class SummaryCreate(SummaryBase):
    book_id: int


class SummaryRead(SummaryBase):
    id: int
    book_id: int
    created_at: datetime
