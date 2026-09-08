#!/bin/bash
set -e

# Install required packages
pip install -r requirements.txt

# Run the tests with coverage
python -m pytest tests/original/ public_tests/ -v --cov=src

echo "All tests completed successfully!"