#!/bin/bash
set -e

echo "Running all Python tests..."
# Discover and run all tests using pytest
pytest
echo "All tests passed."