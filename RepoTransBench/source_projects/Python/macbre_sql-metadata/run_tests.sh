#!/bin/bash
set -e

# Always use Poetry if available, otherwise fallback
if command -v poetry &> /dev/null; then
    poetry install
    poetry run coverage run --branch -m pytest test/
else
    pip install -U pip
    pip install pytest coverage pytest-cov sqlparse
    coverage run --branch -m pytest test/
fi

coverage report --show-missing
coverage html