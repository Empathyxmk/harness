#!/bin/bash
set -e

echo "Building Rust project..."
cargo build

echo "Running original tests..."
cargo test --test=original

echo "Running public tests..."
cargo test --test=public_tests

echo "All tests completed!"