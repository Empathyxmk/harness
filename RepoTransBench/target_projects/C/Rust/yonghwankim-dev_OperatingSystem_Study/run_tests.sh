#!/bin/bash
set -e

# Build and run all Rust tests, both internal and integration/public.
cargo test --all -- --test-threads=1