#!/bin/bash
set -e

# Install project dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Always ensure pytest and coverage are available
pip install pytest coverage pytest-cov

# Run tests with coverage, including branch coverage
coverage run --branch -m pytest timeseriescv/tests
coverage report -m