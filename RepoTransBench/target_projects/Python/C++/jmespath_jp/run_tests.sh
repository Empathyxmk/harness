#!/bin/bash
# Simple one-click build and test script for JMESPath C++ tests

set -e

mkdir -p build
cd build

cmake ..
make

# Run ORIGINAL and PUBLIC test runners (if both are built)
if [ -f ./test_runner ]; then
    echo "Running ORIGINAL tests (tests/original/*)..."
    ./test_runner
else
    echo "Warning: ORIGINAL test runner not found."
fi

if [ -f ./public_test_runner ]; then
    echo "Running PUBLIC tests (public_tests/*)..."
    ./public_test_runner
else
    echo "Warning: PUBLIC test runner not found."
fi