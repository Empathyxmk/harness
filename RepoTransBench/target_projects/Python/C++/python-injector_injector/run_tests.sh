#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running all original tests with test_runner..."
./test_runner
echo "Running all public tests with public_test_runner..."
./public_test_runner