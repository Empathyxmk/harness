#!/bin/bash
set -e

# Build and run all tests (original and public)
dotnet restore
dotnet build

echo "Running original tests..."
dotnet test tests/original/OriginalTests.csproj --no-build --logger:trx

echo "Running public tests..."
dotnet test public_tests/PublicTests.csproj --no-build --logger:trx