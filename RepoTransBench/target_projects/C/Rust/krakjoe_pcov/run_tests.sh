#!/bin/bash
set -e

# This script runs all Rust tests, including original test infrastructure and all staged chunks.
echo "Running all Rust tests for krakjoe_pcov ..."
cargo test --all -- --nocapture