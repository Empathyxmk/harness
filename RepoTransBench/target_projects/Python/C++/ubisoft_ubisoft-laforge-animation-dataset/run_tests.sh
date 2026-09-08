#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running all original C++ tests..."
./test_runner
echo "Running all public C++ tests..."
./public_test_runner