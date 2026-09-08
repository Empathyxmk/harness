#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Fallback: ensure pytest, coverage are available
pip install pytest coverage pytest-cov

# Remove old coverage data
rm -f .coverage

# Run tests with branch coverage
coverage run --branch -m pytest tests

# Show coverage summary and missing lines
coverage report --show-missing

# Generate HTML coverage report for local analysis (optional)
coverage html