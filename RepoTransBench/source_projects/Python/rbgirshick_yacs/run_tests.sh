#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

pip install pytest coverage pytest-cov pyyaml

# Run tests and measure coverage (line and branch)
coverage run --branch -m pytest yacs/tests.py tests/
coverage report -m