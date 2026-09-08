#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make

echo "===== Running Original Tests ====="
./test_runner

echo "===== Running Public Tests ====="
./public_test_runner