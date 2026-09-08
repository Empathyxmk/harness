#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
# Run both original (internal) and public test runners
./test_runner
./public_test_runner