#!/bin/bash
set -e

# Make sure pytest is installed
if ! command -v pytest >/dev/null 2>&1; then
    echo "Installing pytest..."
    pip install pytest
fi

echo "Running all tests..."
pytest tests/
pytest public_tests/