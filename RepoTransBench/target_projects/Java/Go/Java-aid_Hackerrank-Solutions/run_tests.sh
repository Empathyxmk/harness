#!/bin/bash
set -e
# Run all Go tests in the project
go test ./tests/original/... ./public_tests/...