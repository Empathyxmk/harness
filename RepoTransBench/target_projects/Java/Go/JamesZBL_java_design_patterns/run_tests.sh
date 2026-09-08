#!/bin/bash
set -e

# Run all Go tests, both original and public_tests
echo "Running all tests (original and public_tests)..."
go test -v ./tests/original/... ./public_tests/...
echo "All tests completed."