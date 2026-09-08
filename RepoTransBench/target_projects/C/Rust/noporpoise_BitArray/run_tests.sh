#!/bin/bash
set -e

# Build and run all tests (both original and public)
echo "Running all Rust tests (original and public)..."
cargo test --all -- --nocapture
echo "All tests ran successfully."