#!/bin/bash
set -e

echo "Running all Python tests using pytest..."
# Run pytest from the project root to discover tests in both 'tests' and 'public_tests'
pytest --ignore=run_test.sh --ignore=run_public_tests.sh
echo "All tests completed!"