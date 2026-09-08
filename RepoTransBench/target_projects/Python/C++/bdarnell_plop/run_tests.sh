#!/bin/bash
set -e

# Use conan or vcpkg for dependencies if not already present.
# This script assumes GoogleTest is discoverable by CMake.

mkdir -p build
cd build
cmake ..
make

echo "Running original tests:"
./test_runner

echo ""
echo "Running public tests:"
./public_test_runner