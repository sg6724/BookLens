from __future__ import annotations

from typing import Literal

from app.core.config import get_settings


Tone = Literal["casual", "academic", "thriller", "poetic"]
Length = Literal["short", "medium", "detailed"]
Audience = Literal["kids", "teens", "adults"]


def build_prompt(title: str, author: str | None, description: str | None, tone: Tone, length: Length, audience: Audience) -> str:
    meta = f"Title: {title}\nAuthor: {author or 'Unknown'}\nDescription: {description or 'N/A'}\n"
    instructions = (
        "You are BookLens, an expert literary summarizer.\n"
        f"Write a {length} summary for {audience} in a {tone} tone.\n"
        "Avoid spoilers. Keep it safe for the audience.\n"
        "Structure: 1) Title line; 2) 3-7 sentences; 3) Closing takeaway.\n"
    )
    return meta + "\n" + instructions


def summarize_with_gemini(prompt: str) -> str:
    settings = get_settings()
    # Lazy import to avoid heavy deps on startup
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage

    if not settings.GEMINI_API_KEY:
        # Fallback for local dev without key
        return "[DEMO SUMMARY] " + prompt[:300]

    chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GEMINI_API_KEY, temperature=0.7)
    result = chat.invoke([HumanMessage(content=prompt)])
    return result.content  # type: ignore[return-value]
