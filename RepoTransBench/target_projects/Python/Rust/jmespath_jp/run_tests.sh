#!/bin/bash
set -e
# Runs all Rust unit and integration tests including public and original tests.
echo "Running all Rust unit and integration tests..."
cargo test --all --tests