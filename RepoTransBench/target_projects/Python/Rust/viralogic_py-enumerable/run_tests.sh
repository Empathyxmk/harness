#!/bin/bash
set -e
# Run all tests -- both unit (src/tests/) and integration (tests/ and public_tests/)
cargo test --all