#!/bin/bash
set -e

# Run all test files in the test/ directory using node
for file in test/*Test.js; do
  echo "Running $file"
  node "$file"
done

echo "All tests passed."