#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make -j$(nproc)
echo "Running Original Tests..."
./original_tests_runner
echo "Running Public Tests..."
./public_tests_runner