#!/bin/bash
set -e

# Create build directory if not present
mkdir -p build
cd build

# Generate build files and build project
cmake ..
make

# Run test runner
./test_runner