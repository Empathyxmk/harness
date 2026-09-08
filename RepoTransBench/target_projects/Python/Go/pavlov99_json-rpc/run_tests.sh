#!/bin/bash
set -e

# Run all go tests (original and public) across the project, verbose output
go test -v ./...