#!/bin/bash
set -e

echo "Setting up Python environment..."
# Ensure pytest is installed
pip install -r requirements.txt

echo "Running all tests using pytest..."
# Add src directory to PYTHONPATH so modules like 'aes' and 'sha1' can be imported
# Run pytest from the root directory to discover all tests in 'tests/' and 'public_tests/'
PYTHONPATH=./src pytest

echo "All tests completed successfully."