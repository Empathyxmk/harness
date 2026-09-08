#!/bin/bash
set -e

# Build the solution first
dotnet build --configuration Release

# Run original (private) tests
dotnet test tests/original/OriginalTests.csproj --no-build --logger "console;verbosity=normal"

# Run public tests
dotnet test public_tests/PublicTests.csproj --no-build --logger "console;verbosity=normal"