#!/bin/bash
set -e
# Run all Rust tests (including public ones)
cargo test --all -- --nocapture