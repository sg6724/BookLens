from __future__ import annotations

import re
from typing import Iterable


def pick_likely_title(lines: Iterable[str]) -> str | None:
    candidates = []
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        # Prefer lines with many capitalized words
        capitalized_words = re.findall(r"\b[A-Z][a-zA-Z]+\b", clean)
        score = len(capitalized_words) * 2 + len(clean)
        candidates.append((score, clean))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]
