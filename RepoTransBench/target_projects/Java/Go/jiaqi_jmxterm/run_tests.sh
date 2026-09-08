#!/bin/bash
set -e
echo "Running all Go unit tests"
go test ./... -v