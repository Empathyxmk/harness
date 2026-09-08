#!/bin/bash
set -e

echo "--- Setting up Python environment and dependencies ---"
# Ensure pip is installed
python3 -m ensurepip --upgrade || true
# Install pytest
pip install -r requirements.txt

echo "--- Running all translated tests ---"
# Pytest will automatically discover tests in tests/ and public_tests/
# The conftest.py fixture will handle compilation of map.c
pytest

echo "--- All tests executed successfully! ---"