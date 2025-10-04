from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from app.core.config import get_settings


settings = get_settings()

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


async def search_google_books(query: str) -> Optional[Dict[str, Any]]:
    params = {"q": query, "maxResults": 5}
    if settings.GOOGLE_BOOKS_API_KEY:
        params["key"] = settings.GOOGLE_BOOKS_API_KEY
    timeout = httpx.Timeout(10.0, read=20.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(GOOGLE_BOOKS_API_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items") or []
        if not items:
            return None
        # Pick the best scored item
        return items[0]


def extract_book_metadata(item: Dict[str, Any]) -> Dict[str, Any]:
    volume = item.get("volumeInfo", {})
    title = volume.get("title")
    authors = volume.get("authors") or []
    description = volume.get("description")
    image_links = volume.get("imageLinks") or {}
    cover = (
        image_links.get("thumbnail")
        or image_links.get("smallThumbnail")
        or image_links.get("small")
        or image_links.get("medium")
        or image_links.get("large")
        or image_links.get("extraLarge")
    )
    return {
        "title": title,
        "author": ", ".join(authors) if authors else None,
        "description": description,
        "cover_url": cover,
        "google_books_id": item.get("id"),
        "raw": volume,
    }
