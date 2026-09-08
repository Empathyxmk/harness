#!/bin/bash
set -e

# Run original tests
dotnet test tests/original/ --no-build

# Run public tests
dotnet test public_tests/ --no-build