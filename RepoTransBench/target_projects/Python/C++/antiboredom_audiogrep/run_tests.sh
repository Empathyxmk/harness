#!/bin/bash
set -e

# Build and test all C++ test targets
mkdir -p build
cd build
cmake ..
make -j$(nproc)

echo "Running all original tests..."
./test_runner

echo "Running all public tests..."
./public_test_runner