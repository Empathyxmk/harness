#!/bin/bash
set -e
# One-click test runner for Rust version of ssh-audit tests.

echo "=== Running all Rust tests via Cargo ==="
cargo test --all -- --nocapture

exit $?