#!/bin/bash
set -e

echo "Running all tests..."
# pytest automatically discovers tests in `tests/` and `public_tests/`
# as long as they follow naming conventions (test_*.py or *_test.py)
pytest

echo "All tests passed successfully."