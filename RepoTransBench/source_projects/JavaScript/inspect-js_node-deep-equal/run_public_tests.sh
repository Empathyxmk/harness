#!/bin/bash
# Directly run all public tests in 'public_tests' directory using node
for file in ./public_tests/*.public.test.js; do
  echo "Running $file"
  node "$file"
done