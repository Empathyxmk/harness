#!/bin/bash
set -e
echo "==== Running all original and public Rust tests ===="
cargo test --all --test '*' -- --nocapture
echo ""
echo "==== Running public_tests/ directory tests ===="
for file in public_tests/*.rs; do
    # Compile and run single-file test target.
    out="target/tmp_$(basename "$file" .rs)"
    rustc --edition=2021 --test "$file" -o "$out"
    "$out"
done