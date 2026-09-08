#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make -j
echo "Running all original (private) tests..."
./test_runner
echo "Running all public tests..."
./test_public_runner