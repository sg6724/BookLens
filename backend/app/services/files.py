from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple
from uuid import uuid4

from app.core.config import get_settings


settings = get_settings()


def sanitize_filename(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9._-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name or uuid4().hex


def save_upload(content: bytes, original_name: str) -> str:
    safe = sanitize_filename(original_name)
    filename = f"{uuid4().hex}-{safe}"
    path = Path(settings.UPLOAD_DIR) / filename
    path.write_bytes(content)
    return str(path)
