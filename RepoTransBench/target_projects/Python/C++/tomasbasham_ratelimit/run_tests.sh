#!/bin/bash
# C++ test runner for tomasbasham_ratelimit
set -e
mkdir -p build
cd build
cmake ..
make -j$(nproc)
./test_runner