#!/bin/bash
set -e

# Install dependencies if not already present
pip install -r requirements.txt

# Run all tests in both original and public tests
pytest tests/
pytest public_tests/