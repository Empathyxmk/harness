#!/bin/bash
set -e
# Runs all tests across src/, tests/original/, and public_tests/
cargo test --all -- --nocapture