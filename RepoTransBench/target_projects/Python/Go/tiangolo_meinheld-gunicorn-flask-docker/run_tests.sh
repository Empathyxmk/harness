#!/bin/bash
# Simple test execution script for Go translated test suite
set -e

echo "Running all tests (including public and original test translations)..."
go test ./...