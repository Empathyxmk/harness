#!/bin/bash
set -e

# Install dependencies if in a fresh environment
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "Running all Python tests..."
pytest