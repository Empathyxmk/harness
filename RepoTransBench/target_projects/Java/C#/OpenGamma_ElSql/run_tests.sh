#!/bin/bash
set -e
# Build everything (solution, all test projects)
dotnet build OpenGamma.ElSql.sln

# Run original tests
dotnet test tests/original/OpenGamma.ElSql.Tests.csproj

# Run public tests
dotnet test public_tests/OpenGamma.ElSql.PublicTests.csproj

# (You may extend this to aggregate/join reports if desired.)