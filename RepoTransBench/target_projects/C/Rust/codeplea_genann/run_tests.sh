#!/bin/bash
set -e

# Use the default Rust test runner
echo "Running all Rust tests (unit and integration, including public tests)..."
cargo test --all --all-features