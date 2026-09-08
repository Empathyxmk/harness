#!/bin/bash
set -e

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Running all tests using pytest..."
# pytest automatically discovers tests in subdirectories following standard naming conventions (test_*.py or *_test.py)
pytest

echo "All tests finished."