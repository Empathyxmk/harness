#!/bin/bash
set -e

# Run all tests - original and public
echo "Running all tests..."
cargo test --test test_auth_overflow
cargo test --test test_commandline
cargo test --test test_crypt_test
cargo test --test test_dtors_sample
cargo test --path public_tests

echo "All tests completed successfully!"