#!/bin/bash
# Fixed runner script to use node for .mjs test files under __tests__
set -e
for testfile in $(find __tests__ -type f -name '*.test.mjs' | sort); do
  echo "Running $testfile"
  node "$testfile"
done
echo "All existing tests passed."