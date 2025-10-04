from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Book, Summary
from app.db.session import get_db
from app.schemas.summary import SummaryCreate, SummaryRead
from app.services.audio import synthesize_to_mp3
from app.services.embeddings import embed_text
from app.services.summarizer import Audience, Length, Tone, build_prompt, summarize_with_gemini

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.post("", response_model=SummaryRead)
def create_summary(payload: SummaryCreate, db: Session = Depends(get_db)):
    book = db.get(Book, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    prompt = build_prompt(book.title, book.author, book.description, payload.tone, payload.length, payload.audience)
    content = summarize_with_gemini(prompt)

    # Save summary first
    summary = Summary(
        book_id=book.id,
        content=content,
        tone=payload.tone,
        length=payload.length,
        audience=payload.audience,
    )
    db.add(summary)
    db.commit()
    db.refresh(summary)

    # Generate audio
    audio_path = synthesize_to_mp3(content, filename_prefix=f"summary-{summary.id}")
    summary.audio_path = audio_path
    db.add(summary)
    db.commit()
    db.refresh(summary)

    # Embedding and (later) recommender upsert happens in recommendations module
    try:
        vec = embed_text([content])[0]
        # Stored in embeddings table via recommender upsert to keep single source of truth
        from app.services.recommender import recommender

        recommender.upsert(db, book_id=book.id, vector=vec)
    except Exception:
        # Embedding errors shouldn't break API response
        pass

    return summary
