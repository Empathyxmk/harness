#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make -j$(nproc)
echo "Running ALL tests (original and public):"
./test_runner
echo "Running ORIGINAL tests only:"
./original_test_runner
echo "Running PUBLIC tests only:"
./public_test_runner