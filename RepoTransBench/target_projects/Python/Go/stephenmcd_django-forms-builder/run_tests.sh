#!/bin/bash
set -e

echo "==> Running all Go tests (./tests/ and ./public_tests/)..."
go test -v ./tests/... ./public_tests/...