#!/bin/bash
set -e

# Run all tests
cargo test

echo "All frida-detection tests passed."