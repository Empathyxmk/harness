#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
echo "Running ALL original/private tests:"
./test_runner
echo ""
echo "Running ALL public tests:"
./public_test_runner