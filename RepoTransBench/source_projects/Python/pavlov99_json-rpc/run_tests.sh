#!/bin/bash
set -e

# Install dependencies if requirements.txt or setup.py exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

if [ -f "setup.py" ]; then
    pip install .
fi

# Install test dependencies from tox.ini if they exist
if grep -q "\[testenv\]" tox.ini 2>/dev/null; then
    pip install pytest pytest-cov mock
fi

# Run pytest with coverage on the jsonrpc/tests directory
coverage run --branch -m pytest jsonrpc/tests
coverage report --show-missing