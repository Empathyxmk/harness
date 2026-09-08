#!/bin/bash
set -e

cargo test --all --all-targets

echo "If you want to run only original, use 'cargo test --test original'."
echo "If you want to run only public_tests, use 'cargo test --test public_tests'."