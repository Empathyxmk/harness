#!/bin/bash
set -e

if [ ! -d src/CommonsGuy.Cwac.Merge/bin ]; then
    dotnet build CommonsGuy.Cwac.Merge.sln
fi

echo "Running ORIGINAL tests..."
dotnet test tests/original/OriginalTests.csproj --no-build --logger:"console;verbosity=normal"

echo "Running PUBLIC tests..."
dotnet test public_tests/PublicTests.csproj --no-build --logger:"console;verbosity=normal"