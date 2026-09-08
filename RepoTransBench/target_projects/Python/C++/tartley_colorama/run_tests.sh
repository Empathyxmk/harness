#!/bin/bash
set -e

# Usage: ./run_tests.sh
mkdir -p build
cd build
cmake ..
make
echo "Running ORIGINAL tests..."
./test_runner
echo "--------------------------"
echo "Running PUBLIC tests..."
./public_test_runner