#!/bin/bash
set -e

# Run all tests using cargo
cargo test

# Print test results summary
echo "All tests completed successfully!"