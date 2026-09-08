#!/bin/bash
set -e

pip install pytest coverage pytest-cov

# Remove previous coverage files if exist
rm -f .coverage

# Run all tests with coverage (main and extra)
coverage run --branch -m pytest tests.py tests_drawille_extra.py

coverage report

# Also generate HTML coverage report for local dev
coverage html