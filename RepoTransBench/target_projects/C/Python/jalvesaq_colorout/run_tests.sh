#!/bin/bash
# Run all Python tests for the colorout project

set -e

echo "Running tests using pytest..."
pytest -v tests/original/ public_tests/

echo "All tests completed successfully!"