from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Load env from project root if present
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / ".env.example")


class Settings:
    def __init__(self) -> None:
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/booklens.db")
        self.GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
        self.GOOGLE_BOOKS_API_KEY: str | None = os.getenv("GOOGLE_BOOKS_API_KEY")
        self.FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "./data/faiss.index")
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./data/uploads")
        self.AUDIO_DIR: str = os.getenv("AUDIO_DIR", "./data/audio")
        self.COVERS_DIR: str = os.getenv("COVERS_DIR", "./data/covers")
        self.TESSERACT_LANGS: str = os.getenv("TESSERACT_LANGS", "eng")
        self.BACKEND_CORS_ORIGINS: str = os.getenv(
            "BACKEND_CORS_ORIGINS", "http://localhost:5173"
        )

    def ensure_storage(self) -> None:
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.AUDIO_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.COVERS_DIR).mkdir(parents=True, exist_ok=True)
        Path(Path(self.FAISS_INDEX_PATH).parent).mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
