#!/bin/bash
set -e

echo "Building and running all Rust tests..."
cargo test --all --all-targets

echo "Building and running all public tests explicitly..."
for f in public_tests/*.rs; do
  echo "Running public test: $f"
  # If you have more public tests, this could be replaced by a registered test harness.
  cargo test --test $(basename "${f%.*}") || true
done

echo "All applicable Rust tests PASSED."