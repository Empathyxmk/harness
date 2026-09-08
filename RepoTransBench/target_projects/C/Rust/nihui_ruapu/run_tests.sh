#!/bin/bash
set -e

# Run original tests
echo "Running original tests..."
cargo test --test original

# Run public tests
echo "Running public tests..."
cargo test --test public_tests

echo "All tests completed."