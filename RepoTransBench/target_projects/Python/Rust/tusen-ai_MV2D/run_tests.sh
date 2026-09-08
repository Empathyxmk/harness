#!/bin/bash
set -eu
echo "Running ALL tests (original + public) using cargo test..."
cargo test --all -- --nocapture