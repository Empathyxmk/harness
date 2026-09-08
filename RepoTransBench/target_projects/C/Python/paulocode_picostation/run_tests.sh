#!/bin/bash
set -e

# Ensure pytest is installed
if ! command -v pytest &> /dev/null
then
    echo "pytest not found. Installing..."
    pip install pytest
fi

# Run all tests using pytest
echo "Running all tests..."
pytest

echo "All tests finished."