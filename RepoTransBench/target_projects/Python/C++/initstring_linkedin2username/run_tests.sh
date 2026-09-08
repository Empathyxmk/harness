#!/bin/bash
set -e

mkdir -p build
cd build
cmake ..
make
CTEST_OUTPUT_ON_FAILURE=1 ctest