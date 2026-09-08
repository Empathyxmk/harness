#!/bin/bash
set -e

# Run all Rust/Cargo tests (including both original and public tests)
cargo test --all