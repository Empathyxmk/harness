#!/bin/bash
set -e

# Install pytest if not already installed
pip install -r requirements.txt

echo "Running all Python tests using pytest..."
# Run tests from both 'tests/original' and 'public_tests' directories
pytest tests/original/ public_tests/

echo "All tests passed successfully!"