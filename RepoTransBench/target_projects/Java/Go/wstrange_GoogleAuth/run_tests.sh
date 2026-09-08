#!/bin/bash
set -e
echo "=== Running all Go tests (including original and public tests) ==="
go test ./tests/... ./public_tests/...