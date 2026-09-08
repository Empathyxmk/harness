#!/bin/bash
set -e

# Install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Install test dependencies if tox.ini exists
if [ -f "tox.ini" ]; then
    pip install tox
fi

# Ensure pytest is available (default for modern Python test suites)
pip install pytest

# Run tests using pytest for the tests/ directory
pytest tests