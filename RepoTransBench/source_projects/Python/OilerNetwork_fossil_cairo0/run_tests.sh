#!/bin/bash
# Ensure all Python and pytest/coverage dependencies are satisfied
pip install -U setuptools setuptools_scm wheel pytest coverage pytest-cov > /dev/null 2>&1

# Run pytest with full coverage (lines and branches) for all python files in the project except virtualenvs
coverage run --branch -m pytest --maxfail=1 --disable-warnings

# Generate terminal and HTML coverage reports
coverage report --show-missing --skip-covered
coverage html