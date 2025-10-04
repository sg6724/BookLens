from __future__ import annotations

from app.services.books_api import extract_book_metadata


def test_extract_book_metadata():
    item = {
        "id": "abc123",
        "volumeInfo": {
            "title": "Example Book",
            "authors": ["Alice", "Bob"],
            "description": "A sample book.",
            "imageLinks": {"thumbnail": "http://example.com/thumb.jpg"},
        },
    }
    meta = extract_book_metadata(item)
    assert meta["title"] == "Example Book"
    assert meta["author"] == "Alice, Bob"
    assert meta["google_books_id"] == "abc123"
    assert meta["cover_url"].startswith("http")
