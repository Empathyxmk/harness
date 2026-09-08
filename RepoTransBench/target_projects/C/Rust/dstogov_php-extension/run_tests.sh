#!/bin/bash
set -e

# Run all tests (both original and public)
echo "Running all tests..."
cargo test --all

# Display test results
echo "All tests completed!"