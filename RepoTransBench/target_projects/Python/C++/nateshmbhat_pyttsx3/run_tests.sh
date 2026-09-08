#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running all original tests:"
./test_runner
echo "Running all public tests:"
./public_test_runner