#!/bin/bash
set -e

# Run all Go tests in the repository (including both tests/original and public_tests)
go test ./...