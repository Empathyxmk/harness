#!/bin/bash
set -e
echo "Running all Go tests (original + public)..."
go test ./tests/original/... ./public_tests/... -v