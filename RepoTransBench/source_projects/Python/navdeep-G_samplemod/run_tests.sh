#!/bin/bash
set -e

# Install dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run coverage with pytest for full reporting (line and branch)
pytest --cov=sample --cov-branch --cov-report=term-missing --cov-report=html tests/