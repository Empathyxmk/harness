#!/bin/bash
set -e

echo "Building and running all Rust tests"
cargo test --all --all-features -- --nocapture