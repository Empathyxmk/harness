#!/bin/bash
set -e
# Go to script directory, which should be the project root
cd "$(dirname "$0")"
mkdir -p build
cd build
cmake ..
make
./test_runner