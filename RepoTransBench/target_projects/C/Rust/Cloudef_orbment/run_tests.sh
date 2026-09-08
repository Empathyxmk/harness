#!/bin/bash
set -e
# Run both original and public tests.
cargo test --all -- --test-threads=1