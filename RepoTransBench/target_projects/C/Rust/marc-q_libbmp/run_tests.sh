#!/bin/bash
set -e
echo "Running all Rust tests:"
cargo test --all -- --nocapture