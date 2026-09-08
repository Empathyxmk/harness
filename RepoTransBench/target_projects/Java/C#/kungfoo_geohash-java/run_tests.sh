#!/bin/bash
set -e
dotnet restore
dotnet test tests/original/OriginalTests.csproj
dotnet test public_tests/PublicTests.csproj