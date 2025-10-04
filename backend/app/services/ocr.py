from __future__ import annotations

from pathlib import Path
from typing import Optional

import pytesseract

from app.core.config import get_settings
from app.utils.image import preprocess_for_ocr, read_image_bytes


settings = get_settings()


def ocr_image(path: str | Path, lang: Optional[str] = None) -> str:
    image = read_image_bytes(path)
    processed = preprocess_for_ocr(image)
    lang_code = lang or settings.TESSERACT_LANGS
    config = "--psm 11"
    text = pytesseract.image_to_string(processed, lang=lang_code, config=config)
    return text
