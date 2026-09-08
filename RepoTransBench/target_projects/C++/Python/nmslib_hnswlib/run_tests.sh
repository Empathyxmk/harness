#!/bin/bash
set -e
# Run all Python tests (original and public)
echo "Running all Python unit tests"
pytest tests/
pytest public_tests/