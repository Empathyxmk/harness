#!/bin/bash
set -e

# Build solution
dotnet build DevinShine_easyloadingbtn.sln

# Run original tests
dotnet test tests/original/OriginalTests.csproj

# Run public tests
dotnet test public_tests/PublicTests.csproj