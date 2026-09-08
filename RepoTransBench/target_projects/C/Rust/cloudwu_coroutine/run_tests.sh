#!/bin/bash
set -e

echo "Running all coroutine tests:"
cargo test

echo "All coroutine tests passed."