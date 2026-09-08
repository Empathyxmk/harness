#!/bin/bash
set -e

# Run all tests (both original and public)
cargo test

echo "All tests completed successfully!"