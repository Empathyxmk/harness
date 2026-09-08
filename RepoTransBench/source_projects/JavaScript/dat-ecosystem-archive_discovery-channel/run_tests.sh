#!/bin/bash
# Run all existing tests in the ./test directory using Node's built-in test runner (tap)
if [ -d "./test" ]; then
  for f in ./test/*.test.js; do
    echo "Running $f"
    node $f
    if [ $? -ne 0 ]; then
      echo "Test failed: $f"
      exit 1
    fi
  done
else
  echo "No test directory found."
  exit 1
fi
echo "All tests passed."