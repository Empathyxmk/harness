#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make -j
./test_runner
echo "Public test suite:"
./public_test_runner