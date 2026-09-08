#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

pip install pytest coverage pytest-cov

coverage run --branch -m pytest tests
coverage report --show-missing