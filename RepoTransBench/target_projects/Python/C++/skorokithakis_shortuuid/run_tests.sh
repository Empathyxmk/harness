#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running all tests (original and public)..."
./test_runner
./public_test_runner