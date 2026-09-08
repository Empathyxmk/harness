#!/bin/bash
set -e

# Install dependencies (if needed, users can also "pip install -r requirements.txt")
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run all original and public tests with pytest
pytest tests/original
pytest public_tests

# Optionally, you can also run all at once via:
# pytest tests/original public_tests