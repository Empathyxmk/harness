#!/bin/bash
set -e
# Run both standard (`tests`) and public_tests using Rust test conventions
cargo test
# Run tests in public_tests folder, if any exist (in Rust, use [test] in integration test folder)