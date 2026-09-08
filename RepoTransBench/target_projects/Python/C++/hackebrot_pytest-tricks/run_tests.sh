#!/bin/bash
set -e
cd "$(dirname "$0")/hackebrot_pytest-tricks"
mkdir -p build
cd build
cmake ..
make
./test_runner