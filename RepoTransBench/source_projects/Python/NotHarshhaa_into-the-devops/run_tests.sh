#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --quiet pytest coverage pytest-cov

echo "Running syntax and lint tests in tests/syntax_lint.py..."
python3 -m unittest discover -s tests -p 'syntax_lint.py'

echo "Running additional unit tests with coverage..."
coverage run --branch -m pytest tests/test_syntax_lint.py

echo "Generating coverage report..."
coverage report --show-missing
coverage html

echo "All tests executed, coverage.html generated."