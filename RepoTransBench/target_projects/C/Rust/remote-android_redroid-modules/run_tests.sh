#!/bin/bash
set -e

echo "Building and running all tests..."
cargo test -- --nocapture

echo "Tests completed successfully!"