#!/bin/bash
set -e

echo "Installing Python dependencies..."
# Ensure pip is available and up-to-date if needed, though usually available in test environments
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Running all tests using pytest..."
# pytest will discover tests in 'tests/' and 'public_tests/' directories
# It provides clear output by default.
python3 -m pytest