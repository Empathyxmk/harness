#!/bin/bash
set -e

echo "[*] Running all tests"
cargo test --all

echo "Test runner completed."