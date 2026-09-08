#!/bin/bash
set -e
mkdir -p build
cd build
cmake ..
make
# The test binary is typically named test_runner or similar if specified in CMakeLists.txt
if [ -f ./test_runner ]; then
  ./test_runner
else
  # Fallback: find and run any produced test binaries (useful if not named explicitly)
  test_bin=$(find . -maxdepth 1 -type f -executable -name "*test*" | head -n 1)
  if [ -n "$test_bin" ]; then
    $test_bin
  else
    echo "No test binary found. Please ensure target name in CMakeLists.txt matches 'test_runner'."
    exit 1
  fi
fi