#!/bin/bash
# FastAPI Development Setup Script
# Usage: ./scripts/setup.sh

set -e

echo "⚡ Setting up FastAPI development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Install pre-commit hooks
if [ -f .pre-commit-config.yaml ]; then
    echo "🪝 Installing pre-commit hooks..."
    pre-commit install
fi

# Create .env from example if it doesn't exist
if [ ! -f .env ] && [ -f .env.example ]; then
    cp .env.example .env
fi

echo "✅ FastAPI environment ready!"
echo ""
echo "📝 Commands:"
echo "   dev:    uvicorn main:app --reload"
echo "   test:   pytest -v"
echo "   scan:   make grype"