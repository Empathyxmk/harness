#!/bin/bash
set -e
echo "Building and running all Rust tests..."
cargo test --all
echo "All tests passed."