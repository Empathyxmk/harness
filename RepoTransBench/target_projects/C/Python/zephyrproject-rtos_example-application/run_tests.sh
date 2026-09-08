#!/bin/bash
set -e

echo "Setting up Python environment..."
# Create a virtual environment
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
# Install pytest
pip install -r requirements.txt

echo "Running all tests (original and public)..."
# pytest will automatically discover tests in tests/ and public_tests/
# because they are structured as Python packages and test files start with 'test_'
pytest -s # -s to see print statements from tests

echo "Deactivating virtual environment."
deactivate

echo "All tests executed successfully."