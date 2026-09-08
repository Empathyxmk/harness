#!/bin/bash
set -e

# Install dependencies if necessary
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run all tests (original + public)
pytest tests/original/ public_tests/