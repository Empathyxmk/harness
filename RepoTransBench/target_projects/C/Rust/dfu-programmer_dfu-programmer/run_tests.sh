#!/bin/bash
set -e

echo "Running all tests..."
cargo test

# Check if any tests failed
if [ $? -eq 0 ]; then
  echo "All tests passed!"
  exit 0
else
  echo "Some tests failed."
  exit 1
fi