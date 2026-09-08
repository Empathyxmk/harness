#!/bin/bash
set -e

# Install dependencies if requirements exist
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Always ensure pytest, coverage, and dependencies are installed
pip install --upgrade pip setuptools pytest coverage pytest-cov tomli ahocorasick python-json-logger

# Run pytest with coverage for both line and branch coverage
coverage run --branch -m pytest tests
coverage report -m