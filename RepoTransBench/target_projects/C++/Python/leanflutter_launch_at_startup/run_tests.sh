#!/bin/bash
set -e
# Install dependencies if needed
if ! pip show pytest > /dev/null 2>&1; then
    echo "Installing required Python dependencies..."
    pip install -r requirements.txt
fi

echo "Running all tests with pytest..."
pytest tests/original public_tests