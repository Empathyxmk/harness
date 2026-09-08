#!/bin/bash
set -e

# Run original tests
cargo test --test test_math

# Run public tests
cargo test --test test_math_public

echo "All tests completed successfully!"