#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running all tests..."
# pytest automatically discovers tests in 'test_*.py' or '*_test.py' files
# in the current directory and subdirectories.
# Since we have 'tests/' and 'public_tests/', pytest will find them all.
pytest --verbose