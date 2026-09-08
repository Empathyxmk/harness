#!/bin/bash
set -e
# Build and run all tests (including those in tests/ and public_tests/)
cargo test --all -- --test-threads=1