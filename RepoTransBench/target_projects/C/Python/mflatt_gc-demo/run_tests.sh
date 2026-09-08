#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running all tests..."
# Pytest automatically discovers tests in `tests/` and `public_tests/`
# as long as they follow the `test_*.py` naming convention.
pytest -v

echo "All tests completed."