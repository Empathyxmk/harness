#!/bin/bash
set -e

echo "Running Rust unit tests..."

# Run all tests including the public tests
cargo test

echo "Tests completed successfully!"