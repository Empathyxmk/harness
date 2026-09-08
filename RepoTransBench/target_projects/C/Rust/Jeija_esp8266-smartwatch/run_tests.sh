#!/bin/bash
set -e

# Run all original and public Rust tests in one go
echo "Running all esp8266_smartwatch tests..."
cargo test --all --tests