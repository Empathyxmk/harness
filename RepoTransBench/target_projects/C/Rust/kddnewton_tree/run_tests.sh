#!/bin/bash
set -e

# Prepare test directories
bash prepare_test_dirs.sh

# Run all tests
cargo test

echo "All tests completed."