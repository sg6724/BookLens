from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from app.api.v1 import api_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

settings = get_settings()

app = FastAPI(title="BookLens API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_router, prefix="/api/v1")

# Static files for audio
Path(settings.AUDIO_DIR).mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")


@app.on_event("startup")
def on_startup() -> None:
    # Ensure storage directories
    settings.ensure_storage()
    # Create tables if they don't exist (for dev). In prod use Alembic.
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/api/v1/healthz")
