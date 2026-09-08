#!/bin/bash
set -e
mkdir -p build
cd build
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=1
make -j4
echo "Running all tests:"
./test_runner
echo "Running public tests:"
./public_test_runner
echo "Running coverage htmlcov tests (batch 2 and 3):"
# All new coverage-reconstructed tests are linked into test_runner via file glob