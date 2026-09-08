#!/bin/bash
set -e

echo "Building screw tool..."
cargo build --bin screw

echo "Running original tests..."
cargo test --test=original

echo "Running public tests..."
cargo test --test=public_tests

echo "All tests passed!"