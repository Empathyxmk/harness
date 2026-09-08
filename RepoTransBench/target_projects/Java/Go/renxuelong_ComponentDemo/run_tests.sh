#!/bin/bash
set -e
go test ./tests/original/... ./public_tests/... "$@"