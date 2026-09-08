#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make -j

echo "Running original tests:"
./tests/original/test_runner_original
echo "Running public tests:"
./public_tests/test_runner_public