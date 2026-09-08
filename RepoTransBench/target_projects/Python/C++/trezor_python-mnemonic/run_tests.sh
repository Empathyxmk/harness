#!/bin/bash
set -e

# One-click test building and running for all (original + public) tests
mkdir -p build
cd build
cmake ..
make -j
echo "Running original tests:"
./test_runner
echo
echo "Running public tests:"
./public_test_runner