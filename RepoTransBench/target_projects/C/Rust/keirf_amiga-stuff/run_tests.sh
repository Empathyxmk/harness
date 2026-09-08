#!/bin/bash
set -e

# Run all Rust tests including public_tests/
export RUST_TEST_THREADS=1
cargo test --all-targets --all-features

# If you wish to specifically run original/public batches:
# cargo test --test original::*
# cargo test --test public_tests::*