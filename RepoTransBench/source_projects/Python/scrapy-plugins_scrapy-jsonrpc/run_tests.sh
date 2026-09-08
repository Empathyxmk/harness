#!/bin/bash
set -e

# Install dependencies if needed
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || true
fi

pip install pytest coverage pytest-cov mock twisted six || true

# Run tests with coverage (branch)
coverage run --branch -m pytest tests
coverage report -m