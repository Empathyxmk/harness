#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
# Run both test runners (original and public)
echo "Running original tests..."
./original_tests
echo "Running public tests..."
./public_tests