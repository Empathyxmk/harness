#!/bin/bash
set -e

echo "Running all tests for zephyrproject-rtos_example-application..."
cargo test --all

echo
echo "All tests completed successfully!"