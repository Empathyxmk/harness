#!/bin/bash
set -e

# Install dependencies if requirements.txt or use setup.py
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Install test dependencies and the package itself
pip install .

# Run tests with coverage for lines and branches
coverage run --branch -m pytest tests
coverage report --show-missing