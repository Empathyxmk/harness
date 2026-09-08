#!/bin/bash
set -e
# Runs all tests: original and public. By default, runs both Rust test directories.
echo "Running all Rust tests (original and public)..."
cargo test --all --all-targets --all-features