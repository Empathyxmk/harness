#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make -j$(nproc)

echo "Running ORIGINAL tests:"
./test_runner

echo
echo "Running PUBLIC tests:"
./test_public_runner