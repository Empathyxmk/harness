#!/bin/bash
set -e
# Run all tests in both tests/ and public_tests/ (using Rust test conventions)
cargo test --all