#!/bin/bash
set -e
# Run all Rust tests (both original and public)
cargo test --all --tests -- --test-threads=1