#!/bin/bash
set -e

echo "Running all Python tests..."
python -m pytest tests/original public_tests -v

echo "All tests passed successfully."