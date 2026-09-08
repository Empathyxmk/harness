#!/bin/bash
set -e

# Install dependencies if needed
pip install -r requirements.txt --quiet

echo "Running all tests (original and public)..."

# Run original tests
echo "==== Original Tests ===="
python -m pytest -xvs tests/original/ --cov=src --cov-report=term-missing

# Run public tests
echo -e "\n==== Public Tests ===="
python -m pytest -xvs public_tests/ --cov=src --cov-append --cov-report=term-missing

echo -e "\nAll tests completed successfully!"