#!/bin/bash
set -e
echo "Running Rust tests..."
cargo test --all -- --nocapture

if [ -d "public_tests" ]; then
    echo "Running Rust public tests..."
    for testfile in public_tests/*.rs; do
        filename=$(basename -- "$testfile")
        tname="${filename%.*}"
        echo "Testing $filename"
        cargo test --test "$tname" -- --nocapture || true
    done
fi