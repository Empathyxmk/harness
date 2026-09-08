#!/bin/bash
set -e

# Ensure pip dependencies installed
pip install -r requirements.txt

# Run all tests in both 'tests/' and 'public_tests/'
pytest tests/ public_tests/