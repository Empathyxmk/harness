#!/bin/bash
set -e

# Install dependencies if needed
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "Running all Python tests (original and public)..."
pytest tests/original/ public_tests/