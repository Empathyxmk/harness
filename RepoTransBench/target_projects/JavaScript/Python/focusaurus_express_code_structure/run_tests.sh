#!/bin/bash
# Simple test execution script for Python tests

set -e

# Install dependencies if necessary
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run all tests in the project (including tests/ and public_tests/)
pytest