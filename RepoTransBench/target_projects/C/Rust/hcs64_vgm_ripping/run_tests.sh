#!/bin/bash
set -e

echo "Running all tests for hcs64_vgm_ripping..."
# Run all tests (both library tests and integration tests)
cargo test

echo "All tests ran successfully."