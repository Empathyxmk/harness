#!/bin/bash
set -e
echo "Building curl_trurl..."
cargo build

echo "Running all tests (original and public)..."
cargo test --all

echo ""
echo "If you would like to run only original or only public tests, use:"
echo "  cargo test -p curl_trurl --test original"
echo "  cargo test -p curl_trurl --test public_tests"