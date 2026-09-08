#!/bin/bash
set -e

# Ensure you have Google Test and nlohmann_json prior to building!
mkdir -p build
cd build
cmake ..
make -j
./test_runner