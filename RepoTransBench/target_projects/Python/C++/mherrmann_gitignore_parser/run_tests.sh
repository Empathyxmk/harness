#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running ORIGINAL + PUBLIC tests"
./test_runner
./public_test_runner