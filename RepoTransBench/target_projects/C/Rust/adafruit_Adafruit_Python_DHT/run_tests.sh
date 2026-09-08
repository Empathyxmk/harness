#!/bin/bash
set -e
# Simple test execution script for Rust
echo "Running all Rust tests (including public and original)..."
cargo test --all-targets --all-features