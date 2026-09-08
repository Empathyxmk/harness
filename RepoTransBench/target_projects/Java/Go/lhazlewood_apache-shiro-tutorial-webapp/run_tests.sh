#!/bin/bash
set -e

# Find and run ALL Go tests in tests/ and public_tests/
go test ./tests/original/... ./public_tests/...