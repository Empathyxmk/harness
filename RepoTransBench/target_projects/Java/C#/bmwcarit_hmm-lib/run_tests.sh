#!/bin/bash
set -e

dotnet test --no-build tests/original/OriginalTests.csproj
dotnet test --no-build public_tests/PublicTests.csproj