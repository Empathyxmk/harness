#!/bin/bash
set -e

# Run all Rust tests in the workspace, including both original and public translations.
cargo test --all