#!/bin/bash
set -e

# Install test dependencies if needed
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run tests with coverage
coverage run --branch -m unittest discover -s tests -p "test_*.py"
coverage report -m