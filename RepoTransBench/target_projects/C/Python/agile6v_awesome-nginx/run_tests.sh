#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Running all tests..."
# pytest will discover tests in both 'tests/' and 'public_tests/' directories
pytest

echo "All tests passed successfully!"