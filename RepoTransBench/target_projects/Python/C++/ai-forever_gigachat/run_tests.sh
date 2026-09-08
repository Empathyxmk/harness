#!/bin/bash
set -e

BUILD_DIR=build
if [ ! -d "$BUILD_DIR" ]; then
  mkdir "$BUILD_DIR"
fi
cd "$BUILD_DIR"
cmake ..
make
./test_runner