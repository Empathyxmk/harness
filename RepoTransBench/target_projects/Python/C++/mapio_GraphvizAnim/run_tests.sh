#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make -j$(nproc)
echo "Running internal/original tests:"
./test_runner
echo "Running public tests:"
./test_runner_public