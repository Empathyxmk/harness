#!/bin/bash
set -e
# Build and test all original and public test projects
dotnet test tests/original/OriginalTests.csproj
dotnet test public_tests/PublicTests.csproj