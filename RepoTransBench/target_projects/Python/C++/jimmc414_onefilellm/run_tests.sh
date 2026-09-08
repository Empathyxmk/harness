#!/bin/bash
set -e

mkdir -p build
cd build

cmake ..
make

echo -e "\nRunning all tests:"
./test_runner
echo -e "\nRunning all public tests:"
./public_test_runner