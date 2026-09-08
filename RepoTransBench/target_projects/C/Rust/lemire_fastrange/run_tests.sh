#!/bin/bash
set -e

echo "Running all tests for lemire_fastrange..."
cargo test --all

echo "All tests passed successfully."