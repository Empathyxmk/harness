#!/bin/bash
set -e
# Run all Cargo (Rust) tests including tests/ and public_tests via integration test mechanism
cargo test --all