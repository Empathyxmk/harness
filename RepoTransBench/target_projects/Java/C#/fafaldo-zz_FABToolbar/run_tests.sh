#!/bin/bash
set -e

dotnet restore

echo "Running all original and public tests..."
dotnet test tests/original/OriginalTests.csproj
dotnet test public_tests/PublicTests.csproj