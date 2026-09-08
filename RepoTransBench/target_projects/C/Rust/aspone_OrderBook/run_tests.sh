#!/bin/bash
set -e
echo "Running all aspone_orderbook tests (original and public)..."
cargo test --all -- --nocapture