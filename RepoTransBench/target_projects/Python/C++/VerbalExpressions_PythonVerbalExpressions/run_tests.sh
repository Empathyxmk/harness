#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
./test_runner
echo '--- Running public tests ---'
./public_test_runner