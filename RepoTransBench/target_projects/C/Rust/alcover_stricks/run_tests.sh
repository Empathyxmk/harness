#!/bin/bash
set -e
# Rust one-click test execution for all cases (original and public)
cargo test --all -- --nocapture