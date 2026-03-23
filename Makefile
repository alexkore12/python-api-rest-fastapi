# Makefile for python-api-rest-fastapi
# Common development tasks

.PHONY: help install dev test lint security-scan docker-build docker-run clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting"
	@echo "  make security-scan - Run Grype security scan"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make clean        - Clean temporary files"

install:
	pip install -r requirements.txt

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v --cov=. --cov-report=html

lint:
	ruff check . || pylint **/*.py

security-scan:
	bash scripts/security-scan.sh

docker-build:
	docker build -t alexkore12/python-api-fastapi:latest .

docker-run:
	docker-compose up -d

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
