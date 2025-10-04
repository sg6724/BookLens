.PHONY: dev backend frontend test migrate

dev:
	( cd backend && uvicorn app.main:app --reload --port 8000 ) & ( cd frontend && npm run dev )

backend:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -q

migrate:
	cd backend && alembic upgrade head
