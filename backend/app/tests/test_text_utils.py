from __future__ import annotations

from app.utils.text import pick_likely_title


def test_pick_likely_title():
    lines = [
        "some random text",
        "THE GREAT GATSBY",
        "by F. Scott Fitzgerald",
    ]
    title = pick_likely_title(lines)
    assert title is not None
    assert "GATSBY" in title.upper()
