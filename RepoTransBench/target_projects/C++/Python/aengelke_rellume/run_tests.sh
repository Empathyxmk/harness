#!/bin/bash
set -e

# Install pytest if not already
pip install -r requirements.txt

# Run all Python tests (original and public)
pytest tests/original/
pytest public_tests/

echo "All Python tests passed."