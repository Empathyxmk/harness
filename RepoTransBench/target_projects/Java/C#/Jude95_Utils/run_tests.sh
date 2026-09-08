#!/bin/bash
set -e
dotnet build
dotnet test tests/original/OriginalTests.csproj
dotnet test public_tests/PublicTests.csproj