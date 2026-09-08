#!/bin/bash
set -e

# Install requirements if not already installed (optional, remove if handled elsewhere)
if ! pip show pytest > /dev/null 2>&1; then
    echo "pytest not found. Installing requirements..."
    pip install -r requirements.txt
fi

echo "-------------------------------------------"
echo "Running ALL Python tests..."
echo "-------------------------------------------"
pytest
echo "-------------------------------------------"
echo "All tests executed."
echo "-------------------------------------------"