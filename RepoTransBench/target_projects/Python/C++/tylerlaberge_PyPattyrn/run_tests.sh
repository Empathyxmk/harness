#!/bin/bash
set -e

BUILD_DIR="build"
echo "[*] Configuring and building project (CMake + Google Test)..."
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
cmake ..
make -j$(nproc)

echo
echo "[*] Running ALL original/internal tests:"
./bin/test_runner

echo
echo "[*] Running ALL public/educational tests:"
./bin/public_test_runner

echo
echo "[+] All tests executed."
cd ..