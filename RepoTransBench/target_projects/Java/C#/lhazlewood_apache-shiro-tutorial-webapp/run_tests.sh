#!/bin/bash
set -e

# Build src library
dotnet build ./src/HelloShiroProject.csproj

# Run original tests
dotnet test ./tests/original/OriginalTests.csproj --no-build

# Run public tests
dotnet test ./public_tests/PublicTests.csproj --no-build