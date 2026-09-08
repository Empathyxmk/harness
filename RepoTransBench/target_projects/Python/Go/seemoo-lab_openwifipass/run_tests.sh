#!/bin/bash
set -e

# Find all *_test.go in tests/ and run go test
go test ./tests/...