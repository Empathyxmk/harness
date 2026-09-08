#!/bin/bash
set -e

# Install pytest if not already installed
pip install -r requirements.txt

# Run all tests using pytest
# pytest will discover tests in tests/ and public_tests/ directories
echo "Running all tests..."
pytest

echo "All tests completed."