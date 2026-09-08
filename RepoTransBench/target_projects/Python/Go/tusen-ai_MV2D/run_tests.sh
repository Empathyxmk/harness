#!/bin/bash
set -e

echo "Running all Go tests in ./tests/original and ./public_tests..."
go test ./tests/original/... ./public_tests/...