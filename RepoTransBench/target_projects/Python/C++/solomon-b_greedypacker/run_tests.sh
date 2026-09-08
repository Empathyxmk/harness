#!/bin/bash
set -e

# Build and run all tests
mkdir -p build
cd build
cmake ..
make -j
./test_runner