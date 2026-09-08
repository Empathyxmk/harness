#!/bin/bash
set -e

# Set PYTHONPATH for running public tests, similar to private test runner
export PYTHONPATH=$(pwd)/python:$(pwd)/python/liblda:$PYTHONPATH

# Run all public test scripts in the public_tests directory
python3 -m unittest discover -s public_tests -p "test_public_*.py"