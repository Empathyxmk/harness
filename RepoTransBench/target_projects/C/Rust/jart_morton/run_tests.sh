#!/bin/bash
set -e

echo "[run_tests.sh] Running all Rust tests (original + public)..."
cargo test --all --tests