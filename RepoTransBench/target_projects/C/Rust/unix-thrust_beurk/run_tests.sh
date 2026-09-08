#!/bin/bash
set -e

# Run all tests (unit and integration; include public_tests)
echo "==== unix-thrust_beurk: Rust Test Runner ===="
cargo test --all -- --test-threads=1 --nocapture