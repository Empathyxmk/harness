#!/bin/bash
set -e
echo "Running ALL Go tests (original and public)..."
go test ./tests/original/... ./public_tests/... -v