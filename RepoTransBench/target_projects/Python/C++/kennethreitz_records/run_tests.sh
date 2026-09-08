#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
./test_runner
echo "To run public tests: ./public_test_runner"