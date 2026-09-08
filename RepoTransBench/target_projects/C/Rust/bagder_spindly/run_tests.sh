#!/bin/bash
set -e

# Run all tests - both original and public tests
cargo test

echo "All tests executed successfully!"