#!/bin/bash
set -e

# One-click Rust test execution script
echo "Building and running all tests..."
cargo test --all-targets --all-features