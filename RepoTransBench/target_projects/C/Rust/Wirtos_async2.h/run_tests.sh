#!/bin/bash
set -e

# Run all tests
cargo test

# Run public tests specifically
echo "Running public tests..."
cargo test --test public_tests