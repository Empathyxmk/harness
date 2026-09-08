#!/bin/bash
# Simple test execution script for Go tests
set -e

# Run all Go tests, recursively, in both tests/original and public_tests
go test ./tests/original/... ./public_tests/...