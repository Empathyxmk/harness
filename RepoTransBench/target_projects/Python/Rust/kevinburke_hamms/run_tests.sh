#!/bin/bash
set -e
cargo test --all --tests -- --nocapture
cargo test --test '*' -- --nocapture
cargo test --manifest-path Cargo.toml -- --nocapture