#!/bin/bash
set -e
cargo test --all --all-targets "$@"