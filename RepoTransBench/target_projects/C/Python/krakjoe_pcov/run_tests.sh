#!/bin/bash
set -e

echo "Setting up Python environment and installing dependencies..."
# Ensure pip is up-to-date and install requirements
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running all Python tests using pytest..."
# Run tests in both the 'tests/original' and 'public_tests' directories.
# pytest automatically discovers 'test_*.py' files and runs functions/methods
# starting with 'test_'.
pytest tests/original/ public_tests/