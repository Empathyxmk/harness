#!/bin/bash
set -e

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo
echo "Running all Python tests with pytest..."
# pytest will automatically discover tests in 'tests/' and 'public_tests/'
# if they follow the 'test_*.py' or '*_test.py' naming convention.
pytest