#!/bin/bash
set -e
# This script runs all Go tests in both original and public test directories
go test ./tests/original/... ./public_tests/... -v