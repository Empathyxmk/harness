#!/bin/bash
set -e
echo "Running all tests (original and public)..."
go test ./tests/original/... ./public_tests/...