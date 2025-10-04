from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class EmbeddingRead(BaseModel):
    id: int
    book_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
