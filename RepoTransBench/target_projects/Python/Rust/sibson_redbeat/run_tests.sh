#!/bin/bash
set -e
cargo test --all --all-features --color always "$@"