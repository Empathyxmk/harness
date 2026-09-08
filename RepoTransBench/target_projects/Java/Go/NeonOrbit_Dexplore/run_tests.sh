#!/bin/bash
set -e

echo "Running all Go tests..."

go test ./tests/original/... ./public_tests/...

echo "Done."