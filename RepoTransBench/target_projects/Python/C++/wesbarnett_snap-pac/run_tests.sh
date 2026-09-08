#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make -j$(nproc)
echo "Running original tests..."
./test_runner
echo "Running public tests..."
./public_test_runner