# BookLens

AI-powered book companion web application

## Tech Stack
- Backend: FastAPI, SQLAlchemy, Alembic, Tesseract OCR, OpenCV, LangChain + Gemini, Sentence Transformers, FAISS, gTTS
- Frontend: React + Vite + TypeScript
- Database: SQLite

## Setup (local)
1. Python 3.11 and Node 18+ required.
2. Copy `.env.example` to `.env` and fill secrets.
3. Backend:
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r backend/requirements.txt`
   - `cd backend && alembic upgrade head`
   - `uvicorn app.main:app --reload --port 8000`
4. Frontend:
   - `cd frontend && npm install && npm run dev`

Backend docs: `http://localhost:8000/docs`
Frontend: `http://localhost:5173`

## Docker
```
docker-compose up --build
```

## Notes
- Audio files served under `/audio`.
- Without `GEMINI_API_KEY`, summaries return deterministic demo text.
