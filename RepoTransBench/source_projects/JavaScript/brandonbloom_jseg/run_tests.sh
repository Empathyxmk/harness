#!/bin/bash
set -e

# Use NYC for coverage and run both legacy node test/index.js and new direct test files
echo "Running legacy tests via 'node test'"
node test

echo "Running additional direct coverage tests"
for f in test/*_coverage.js; do
  echo "Running $f"
  node "$f"
done