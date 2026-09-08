#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Running all tests..."
# Run pytest from the root, it will discover tests in tests/ and public_tests/
pytest --verbose

echo "All tests complete."