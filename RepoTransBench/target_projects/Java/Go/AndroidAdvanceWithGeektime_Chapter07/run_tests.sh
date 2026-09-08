#!/bin/bash
# Simple test runner for all original and public tests.
set -e
go test ./tests/original/... ./public_tests/...