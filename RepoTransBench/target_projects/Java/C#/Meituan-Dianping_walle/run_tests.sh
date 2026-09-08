#!/bin/bash
set -e

# Build everything
dotnet build

# Run all original tests
dotnet test tests/original/OriginalTests.csproj

# Run all public tests
dotnet test public_tests/PublicTests.csproj