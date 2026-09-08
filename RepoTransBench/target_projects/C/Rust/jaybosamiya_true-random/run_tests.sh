#!/bin/bash
set -e

# Build and run the main library tests
echo "Running library tests..."
cargo test

# Build and run the public tests
echo "Running public tests..."
cargo test --test test_true_random --test test_constant_stream

# Run the public test binary
echo "Running public test binary (15 random numbers)..."
cargo run --bin public_test_true_random

# Run the public stream generator
echo "Running public stream generator (20 random bytes)..."
cargo run --bin public_generate_constant_stream | xxd

echo "All tests passed."