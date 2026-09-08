#!/bin/bash
set -e

echo "Installing test dependencies..."
pip install -r requirements.txt

echo "Running all tests using pytest..."
# pytest automatically discovers tests in 'tests/' and 'public_tests/' directories
pytest

echo "All tests executed."