#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make -j$(nproc)
echo "========== Running Original Tests =========="
./test_runner
echo ""
echo "========== Running Public Tests ============"
./test_runner_public