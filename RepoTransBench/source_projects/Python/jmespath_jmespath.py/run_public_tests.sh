#!/bin/bash
set -e

# Ensure pytest is installed
pip install "pytest==6.2.5"

# Run public tests
python -m pytest public_tests