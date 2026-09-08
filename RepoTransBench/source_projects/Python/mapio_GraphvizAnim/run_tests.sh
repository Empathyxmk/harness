#!/bin/bash
set -e

# Install dependencies from binder/requirements.txt if present
if [ -f binder/requirements.txt ]; then
    pip install -r binder/requirements.txt
fi

pip install pytest pytest-timeout pytest-cov coverage

# Run tests with coverage
coverage run --branch -m pytest --timeout=10 tests/
coverage report -m
coverage html