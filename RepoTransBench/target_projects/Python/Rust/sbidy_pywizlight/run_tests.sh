#!/bin/bash
set -e

# Run all Rust tests in both ./tests and ./public_tests
cargo test --all