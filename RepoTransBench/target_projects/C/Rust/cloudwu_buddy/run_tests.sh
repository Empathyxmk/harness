#!/bin/bash
set -e

# Run all Rust tests (including both /tests and /public_tests if using #[test])
cargo test --all -- --nocapture