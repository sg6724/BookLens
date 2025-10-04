from __future__ import annotations

from pathlib import Path
from typing import Optional
from uuid import uuid4

from gtts import gTTS

from app.core.config import get_settings


settings = get_settings()


def synthesize_to_mp3(text: str, filename_prefix: Optional[str] = None) -> str:
    base = filename_prefix or uuid4().hex
    file_path = Path(settings.AUDIO_DIR) / f"{base}.mp3"
    tts = gTTS(text)
    tts.save(str(file_path))
    return str(file_path)
