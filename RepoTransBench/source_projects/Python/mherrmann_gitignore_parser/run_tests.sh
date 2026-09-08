#!/bin/bash
set -e

# Skip pip install if pip is broken.
# Run coverage only if coverage is installed and gitignore_parser.py exists.

if ! command -v coverage >/dev/null 2>&1; then
    echo "coverage.py is not installed; cannot run tests with coverage."
    exit 1
fi

coverage run --branch -m unittest tests.py extra_tests.py
coverage report --show-missing