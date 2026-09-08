#!/bin/bash
set -e
echo "Running all Go tests (including original and public)..."
go test ./tests/original/... ./public_tests/...