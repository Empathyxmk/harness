#!/bin/bash
set -e

# Install requirements if necessary (comment out if you use a virtualenv)
pip install -r requirements.txt

# Run pytest over all test directories
pytest tests/ public_tests/