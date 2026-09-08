#!/bin/bash
set -e

# Install dependencies if in a clean environment
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run public tests
echo "========== Running public tests =========="
pytest public_tests

# Run original tests
echo "========== Running original tests =========="
pytest tests/original