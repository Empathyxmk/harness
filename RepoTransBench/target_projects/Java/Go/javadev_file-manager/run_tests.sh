#!/bin/bash
set -e

echo "Running all Go FileManager tests..."
go test ./...
echo "All tests completed."