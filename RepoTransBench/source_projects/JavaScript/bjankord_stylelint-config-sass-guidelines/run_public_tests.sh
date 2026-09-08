#!/bin/bash
# Run all public tests in the public_tests/ directory using Node
set -e
for file in public_tests/*.public.test.mjs; do
  echo "Running $file"
  node "$file"
done
echo "All public tests passed."