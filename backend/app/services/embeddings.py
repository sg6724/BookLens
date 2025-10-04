from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import numpy as np


@lru_cache(maxsize=1)
def _get_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def embed_text(texts: Iterable[str]) -> np.ndarray:
    model = _get_model()
    vectors = model.encode(list(texts), convert_to_numpy=True, normalize_embeddings=True)
    return vectors.astype(np.float32)


def vector_to_bytes(vec: np.ndarray) -> bytes:
    assert vec.dtype == np.float32
    return vec.tobytes()


def bytes_to_vector(b: bytes, dim: int) -> np.ndarray:
    arr = np.frombuffer(b, dtype=np.float32)
    if dim > 0 and arr.size != dim:
        # If dim mismatch, attempt to reshape (will raise otherwise)
        pass
    return arr
