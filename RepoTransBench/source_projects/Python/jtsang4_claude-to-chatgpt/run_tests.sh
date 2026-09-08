#!/bin/bash
set -e

# Install dependencies if needed
pip install --upgrade pip
pip install poetry pytest pytest-cov httpx fastapi tiktoken

# Install project dependencies
if [ -f "pyproject.toml" ]; then
    poetry install
fi

# Run pytest with branch and line coverage, show missing lines/branches
pytest --cov=claude_to_chatgpt --cov-report=term-missing --cov-report=html --cov-branch tests