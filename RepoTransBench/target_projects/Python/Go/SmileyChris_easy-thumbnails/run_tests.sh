#!/bin/bash
set -e

echo "Running all Go tests (original and public test suites)..."
go test ./tests/original/... ./public_tests/... -v