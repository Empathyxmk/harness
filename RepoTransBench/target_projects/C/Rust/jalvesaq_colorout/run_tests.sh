#!/bin/bash
# Run all Rust tests for the jalvesaq_colorout project

set -e

echo "Running all tests..."
cargo test

echo "All tests completed!"