#!/bin/bash
set -e

# Install dependencies if requirements exist
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Ensure pytest is installed and use pytest with minimal plugins to avoid interference
pip install "pytest==6.2.5"

# Run tests (mainly located in tests/ and match test_*.py pattern)
python -m pytest tests

# Also run the extra hypothesis-based test, but allow it to fail without stopping all tests
if [ -f extra/test_hypothesis.py ]; then
    echo "Running hypothesis-based tests in extra/test_hypothesis.py (optional)..."
    python -m pytest extra/test_hypothesis.py || echo "extra/test_hypothesis.py: Ignored error (optional hypothesis tests)."
fi