#!/bin/bash
set -e

# Restore packages; build solution; run all tests
dotnet restore
dotnet build --no-restore
dotnet test --no-build tests/original/OriginalTests.csproj
dotnet test --no-build public_tests/PublicTests.csproj