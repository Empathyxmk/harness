#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running all tests with pytest..."
# Run tests from both original and public directories.
# pytest automatically discovers tests in directories named 'test_*'
# and files named 'test_*.py' or '*_test.py', and functions/methods named 'test_*'.
pytest tests/original public_tests

echo "All Python tests passed!"