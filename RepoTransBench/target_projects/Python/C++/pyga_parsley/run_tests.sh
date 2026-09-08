#!/bin/bash
set -e

echo "Building and running all C++ tests (original + public)..."

mkdir -p build
cd build
cmake ..
make
./test_runner