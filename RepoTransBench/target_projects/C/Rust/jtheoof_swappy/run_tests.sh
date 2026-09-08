#!/bin/bash
set -e

# Run original tests
cargo test --test algebra --test file -- --nocapture