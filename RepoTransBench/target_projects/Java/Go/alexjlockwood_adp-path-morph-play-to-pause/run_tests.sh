#!/bin/bash
set -e

echo "Running all Go tests in original/ and public_tests/..."
go test ./...