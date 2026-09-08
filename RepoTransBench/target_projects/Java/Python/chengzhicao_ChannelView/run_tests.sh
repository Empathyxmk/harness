#!/bin/bash
set -e

# Ensure dependencies are installed
if ! python -c "import pytest" 2>/dev/null; then
    echo "pytest not found; installing dependencies..."
    pip install -r requirements.txt
fi

echo "[INFO] Running all tests (original and public)..."
pytest tests/original public_tests