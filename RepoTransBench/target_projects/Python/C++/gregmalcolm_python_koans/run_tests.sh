#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make -j$(nproc || sysctl -n hw.ncpu || echo 2)
echo "Running original tests:"
./test_runner
echo ""
echo "Running public tests:"
./public_test_runner