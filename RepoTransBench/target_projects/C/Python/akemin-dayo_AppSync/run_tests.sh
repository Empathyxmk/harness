#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running all tests..."
# pytest automatically discovers tests in 'tests/' and 'public_tests/' directories
# It also includes subdirectories by default
pytest

echo "All tests passed!"