#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running all tests with pytest..."
pytest

echo "All tests passed!"