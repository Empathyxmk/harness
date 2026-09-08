#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running all original test cases..."
./test_runner
echo "Running all public test cases..."
./test_runner_public