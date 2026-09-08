#!/bin/bash
set -e

echo "Running Python tests..."

# Install required dependencies if needed
pip install -r requirements.txt

# Run original tests
echo "Running original tests..."
python -m pytest tests/original -v

# Run public tests
echo "Running public tests..."
python -m pytest public_tests -v

echo "All tests completed."