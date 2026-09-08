#!/bin/bash
set -e

# Runs all original and public Go tests (recursively)
go test ./... -v