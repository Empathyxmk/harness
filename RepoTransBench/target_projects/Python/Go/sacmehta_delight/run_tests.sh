#!/bin/bash
set -e
echo "Running all Go tests..."
# Run original (internal) tests
go test -v ./tests/...
# Run public tests (if they exist)
if [ -d "./public_tests" ]; then
    go test -v ./public_tests/...
fi