#!/bin/bash
set -e
echo "[Running ALL Go tests in ./tests/ and ./public_tests/]"
go test -v ./tests/... ./public_tests/...