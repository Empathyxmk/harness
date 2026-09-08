#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Try pytest first, else fall back to unittest discover
if python -m pytest --maxfail=1 --disable-warnings test/; then
    exit 0
else
    python -m unittest discover -s test -p "test_*.py"
fi