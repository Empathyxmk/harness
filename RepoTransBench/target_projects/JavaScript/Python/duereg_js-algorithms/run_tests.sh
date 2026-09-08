#!/bin/bash
set -e
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
# Run original tests
pytest tests/
# Run public tests
pytest public_tests/