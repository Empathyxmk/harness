#!/bin/bash
set -e

# Run all Go tests in the project (including main, tests, and public_tests)
go test ./...