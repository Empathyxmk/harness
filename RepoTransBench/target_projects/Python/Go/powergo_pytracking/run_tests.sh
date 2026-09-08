#!/bin/bash
set -e

# Discover and run ALL Go tests (recursively, including tests/original/, public_tests/, etc.)
go test ./...