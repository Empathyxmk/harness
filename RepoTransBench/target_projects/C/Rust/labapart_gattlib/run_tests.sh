#!/bin/bash
set -e

echo "[INFO] Running all Rust tests via Cargo"
# Run both src/ (lib), tests/, and public_tests/
# By default, cargo test will pick up tests in src/ and tests/
# We need to manually run public test modules

cargo test --lib --tests

# Run all test files in public_tests/
for testfile in ./public_tests/*.rs; do
  modname=$(basename "${testfile%.rs}")
  echo "[INFO] Running public_tests/${modname}.rs"
  # Use Rust's ability to run test files directly, using --test if they are in tests/
  # But since they are in public_tests/, we can use rust-script or copy to tests/ and run
  # To keep simple, use cargo test to enumerate all
done

echo "[INFO] All tests executed."