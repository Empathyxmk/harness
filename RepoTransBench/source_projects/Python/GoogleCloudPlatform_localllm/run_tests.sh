#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Install core test/coverage tools
pip install pytest coverage pytest-cov

# Run all tests in local-llm, including new comprehensive suite
echo "Running pytest with coverage"
coverage run --branch -m pytest local-llm/ --disable-warnings
coverage report
coverage html