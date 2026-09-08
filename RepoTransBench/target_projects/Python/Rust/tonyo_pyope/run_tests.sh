#!/bin/bash
set -e
echo "Running all tests with cargo..."
cargo test --all -- --nocapture