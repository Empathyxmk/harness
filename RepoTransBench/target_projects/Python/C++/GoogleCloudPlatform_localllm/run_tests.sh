#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make

echo "Running original test suite..."
./test_runner

echo "Running public test suite..."
./public_test_runner