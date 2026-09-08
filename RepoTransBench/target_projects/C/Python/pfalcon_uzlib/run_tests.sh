#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Running all Python tests with pytest..."
# Run original tests
echo "Running original tests..."
pytest tests/original/

# Run public tests
echo "Running public tests..."
pytest public_tests/

echo "All tests passed successfully."