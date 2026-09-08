#!/bin/bash

set -e

# Run original tests in ./tests/... and public tests in ./public_tests/...
echo "Running original tests..."
go test -v ./tests/...

echo "Running public tests..."
go test -v ./public_tests/...