#!/bin/bash
set -e

echo "[Rust Test Runner] Running all tests (original and public)..."
cargo test --all