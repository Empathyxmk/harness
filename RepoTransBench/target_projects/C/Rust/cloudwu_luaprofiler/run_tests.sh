#!/bin/bash
set -e

echo "Building and running tests for luaprofiler Rust project..."

# Build the project
cargo build

# Run original tests
echo "Running original tests..."
cargo test --package luaprofiler --test test_profiler

# Run public tests
echo "Running public tests..."
cargo run --bin public_test

echo "All tests completed."