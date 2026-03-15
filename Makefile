.PHONY: help install dev backend frontend test seed docker-up docker-down clean

help:
	@echo "Nexus CRM - Available commands:"
	@echo "  make install      - Install all dependencies"
	@echo "  make dev          - Start development servers"
	@echo "  make backend      - Start backend server"
	@echo "  make frontend     - Start frontend server"
	@echo "  make test         - Run all tests"
	@echo "  make seed         - Seed database with sample data"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make clean        - Clean generated files"

install:
	cd backend && python -m venv venv && venv/Scripts/pip install -r requirements.txt
	cd frontend && npm install

dev:
	@echo "Starting backend and frontend..."
	$(MAKE) backend &
	$(MAKE) frontend

backend:
	cd backend && venv/Scripts/uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && venv/Scripts/pytest tests/ -v

seed:
	cd backend && venv/Scripts/python -m app.seed

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

clean:
	rm -rf backend/venv backend/__pycache__ backend/.pytest_cache
	rm -rf frontend/node_modules frontend/dist
	rm -f backend/test.db
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
