#!/bin/bash
set -e

# Install dependencies
pip install -r requirements.txt

# Run all tests using pytest
# pytest will discover tests in tests/ and public_tests/ by default
pytest