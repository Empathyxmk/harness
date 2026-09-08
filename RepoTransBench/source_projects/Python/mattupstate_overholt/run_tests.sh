#!/bin/bash
set -e

pip install --upgrade pip
pip install -r requirements.txt
pip install pytest coverage pytest-cov

# Clean previous coverage
coverage erase

# Run tests with coverage (include branch reporting)
coverage run --branch -m pytest tests

# Show report
coverage report --show-missing
coverage html