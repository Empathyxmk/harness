#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run pytest with coverage for tests/ and report
coverage run --branch --source=wpanalyser -m pytest tests/
coverage report -m