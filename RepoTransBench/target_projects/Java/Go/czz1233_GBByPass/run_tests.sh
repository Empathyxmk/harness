#!/bin/bash
set -e
echo "Running all tests"
go test ./company/... ./tests/original/... ./public_tests/... -v