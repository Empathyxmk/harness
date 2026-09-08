#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make

echo "Running original tests:"
./original_tests_runner

echo "Running public tests:"
./public_tests_runner