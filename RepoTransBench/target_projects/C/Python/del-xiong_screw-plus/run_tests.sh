#!/bin/bash
set -e

echo "Running Python unit tests for base64 encode/decode..."

# Install dependencies if not already installed
pip install -r requirements.txt

# Run all tests with coverage
pytest tests/original/ public_tests/ -v --cov=src --cov-report=term-missing

echo "All tests completed successfully!"