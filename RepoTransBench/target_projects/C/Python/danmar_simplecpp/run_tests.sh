#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running all tests..."
pytest

echo "All tests completed successfully."