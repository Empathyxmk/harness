#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Install test dependencies if test-requirements.txt exists
if [ -f test-requirements.txt ]; then
    pip install -r test-requirements.txt
fi

# Ensure pytest + coverage is installed
pip install pytest coverage pytest-cov

# Run all tests in the tests/ directory with branch coverage
coverage run --branch -m pytest tests
coverage report --show-missing