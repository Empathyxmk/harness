#!/bin/bash

set -e
echo "Running all tests with Cargo..."
cargo test

echo "All tests passed!"