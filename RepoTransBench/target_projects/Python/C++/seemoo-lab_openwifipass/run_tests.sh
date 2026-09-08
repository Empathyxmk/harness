#!/bin/bash
set -e

echo "=== Building and Running All Tests (Original and Public) ==="

mkdir -p build
cd build

cmake ..
make

echo "Running ALL original tests:"
./test_runner

echo "Running ALL public tests:"
./public_test_runner