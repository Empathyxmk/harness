#!/bin/bash
set -e

echo "Running all Python tests using pytest..."

# Run pytest from the root directory.
# pytest automatically discovers test files named `test_*.py` or `*_test.py`
# in the current directory and its subdirectories.
# This setup will discover tests in 'tests/original/' and 'public_tests/'.
pytest

echo "All tests completed successfully."