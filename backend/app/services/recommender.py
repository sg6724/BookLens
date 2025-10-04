from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import List, Tuple

import faiss  # type: ignore
import numpy as np
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Book, Embedding


class Recommender:
    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self.map_path = self.index_path.with_suffix(".map.json")
        self.lock = threading.Lock()
        self.index: faiss.Index | None = None
        self.book_ids: list[int] = []

    def _create_index(self, dim: int) -> faiss.Index:
        # Cosine similarity via inner product on normalized vectors
        index = faiss.IndexFlatIP(dim)
        return index

    def _save(self) -> None:
        assert self.index is not None
        faiss.write_index(self.index, str(self.index_path))
        self.map_path.write_text(json.dumps(self.book_ids))

    def _load(self) -> bool:
        if not self.index_path.exists() or not self.map_path.exists():
            return False
        self.index = faiss.read_index(str(self.index_path))
        self.book_ids = json.loads(self.map_path.read_text())
        return True

    def rebuild_from_db(self, db: Session) -> None:
        with self.lock:
            rows = db.query(Embedding).all()
            if not rows:
                self.index = None
                self.book_ids = []
                # Ensure directory exists
                self.index_path.parent.mkdir(parents=True, exist_ok=True)
                return
            vectors = [np.frombuffer(r.embedding, dtype=np.float32) for r in rows]
            dim = vectors[0].shape[0]
            index = self._create_index(dim)
            index.add(np.vstack(vectors))
            self.index = index
            self.book_ids = [r.book_id for r in rows]
            self._save()

    def ensure_loaded(self, db: Session) -> None:
        with self.lock:
            if self.index is not None:
                return
            if not self._load():
                self.rebuild_from_db(db)

    def upsert(self, db: Session, book_id: int, vector: np.ndarray) -> None:
        # To keep logic simple and robust, rebuild index upon upsert
        # on small datasets this is fine
        existing = db.query(Embedding).filter(Embedding.book_id == book_id).first()
        if existing:
            existing.embedding = vector.tobytes()
        else:
            db.add(Embedding(book_id=book_id, embedding=vector.tobytes()))
        db.commit()
        self.rebuild_from_db(db)

    def recommend(self, db: Session, book_id: int, top_k: int = 5) -> List[int]:
        self.ensure_loaded(db)
        if self.index is None or not self.book_ids:
            return []
        try:
            idx = self.book_ids.index(book_id)
        except ValueError:
            return []
        vector = self.index.reconstruct(idx)
        D, I = self.index.search(np.expand_dims(vector, 0), min(top_k + 1, len(self.book_ids)))
        neighbors: list[int] = []
        for j in I[0].tolist():
            if j == -1:
                continue
            bid = self.book_ids[j]
            if bid != book_id:
                neighbors.append(bid)
        return neighbors[:top_k]


_settings = get_settings()
recommender = Recommender(_settings.FAISS_INDEX_PATH)
