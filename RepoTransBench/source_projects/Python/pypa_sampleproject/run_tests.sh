#!/bin/bash
set -e

# Remove existing .coverage data
rm -f .coverage

# Uninstall problematic pytest-cov version
pip uninstall -y pytest-cov || true

# Install compatible versions of test/coverage tools
pip install "pytest>=8.0.0,<9.0.0" "coverage>=7.0.0,<8.0.0"

# Run tests with coverage (branch coverage enabled)
coverage run --branch -m pytest --maxfail=1 --disable-warnings -v
coverage report -m