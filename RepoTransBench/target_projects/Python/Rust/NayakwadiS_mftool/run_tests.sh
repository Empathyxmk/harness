#!/bin/bash
set -e
# Make sure public_tests/* are run by including a mod.rs file, or run using bin target if needed
cargo test --all