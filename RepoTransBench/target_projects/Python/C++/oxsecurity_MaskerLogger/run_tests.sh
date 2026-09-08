#!/bin/bash
set -e

# Build using CMake
mkdir -p build
cd build
cmake ..
make

# Run all tests
./test_runner