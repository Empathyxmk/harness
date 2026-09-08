#!/bin/bash
set -e

# Ensure pytest is installed
if ! command -v pytest &> /dev/null
then
    echo "pytest not found. Installing..."
    pip install pytest
fi

echo "Running all tests (original and public)..."
pytest

echo "All tests passed successfully."
exit 0