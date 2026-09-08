#!/bin/bash
set -e
# Run all Rust tests (original and public)
cargo test --all -- --nocapture
echo ""
echo "Public test module(s):"
cargo test --test pipe_public_test -- --nocapture || echo "No public_tests/ executable found."