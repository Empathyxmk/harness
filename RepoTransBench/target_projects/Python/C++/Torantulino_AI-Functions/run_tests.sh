#!/bin/bash
set -e

# One-click build & run all tests via CMake and GoogleTest
mkdir -p build
cd build
cmake ..
make
./test_runner