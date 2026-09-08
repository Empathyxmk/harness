#!/bin/bash
set -e

# Run all tests in public_tests/ and tests/ (if any)
pytest public_tests/
if [ -d "tests/original" ]; then
    pytest tests/original/
elif [ -d "tests" ]; then
    pytest tests/
fi