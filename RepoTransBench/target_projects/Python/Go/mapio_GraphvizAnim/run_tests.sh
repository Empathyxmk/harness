#!/bin/bash
set -e
# Run all Go tests in all packages and subdirectories (both tests and public_tests)
go test ./...