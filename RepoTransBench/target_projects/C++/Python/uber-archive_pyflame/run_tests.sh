#!/bin/bash
set -e

# Install dependencies (in user context, harmless if already installed)
pip install --quiet -r requirements.txt

# Run all tests: original and public
pytest tests/original/
pytest public_tests/