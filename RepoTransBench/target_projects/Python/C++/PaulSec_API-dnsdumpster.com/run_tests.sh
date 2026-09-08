#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running ALL ORIGINAL and PUBLIC tests:"
./test_runner
./public_test_runner