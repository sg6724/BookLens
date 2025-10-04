from __future__ import annotations

from fastapi import APIRouter

from . import health, books, summaries, recommendations, library

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(books.router)
api_router.include_router(summaries.router)
api_router.include_router(recommendations.router)
api_router.include_router(library.router)
