#!/bin/bash
set -e
# Run all Go tests in subdirectories, including original and public_tests
go test ./...