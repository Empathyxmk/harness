#!/bin/bash
set -e

echo "Installing test dependencies..."
pip install -r requirements.txt

echo "Running all tests (original and public)..."
# Pytest automatically discovers tests in subdirectories
# Add src to PYTHONPATH so that 'from quadprog import ...' imports work
# if a `quadprog` module is present in src/
PYTHONPATH=./src:$PYTHONPATH pytest tests/original/ public_tests/

echo "All tests completed."