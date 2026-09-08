#!/bin/bash
set -e
cargo test --workspace --all-targets "$@"