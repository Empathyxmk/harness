#!/bin/bash
set -e

# Install dependencies if requirements.txt or pyproject.toml exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    pip install .
fi

# Run all tests with coverage (line & branch) and create report
coverage run --branch -m pytest tests
coverage report