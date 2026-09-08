#!/bin/bash
set -e
echo "Running all Go tests (original and public)..."
go test -v ./tests/original/... ./public_tests/...