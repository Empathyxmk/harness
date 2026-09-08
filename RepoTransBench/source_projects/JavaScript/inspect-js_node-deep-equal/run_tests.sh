#!/bin/bash
# Directly run all tests in 'test' directory using node
for file in ./test/*.test.js; do
  echo "Running $file"
  node "$file"
done