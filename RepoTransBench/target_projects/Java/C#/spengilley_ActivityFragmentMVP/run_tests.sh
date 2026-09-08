#!/bin/bash
set -e
dotnet restore spengilley_ActivityFragmentMVP.sln
dotnet build spengilley_ActivityFragmentMVP.sln
dotnet test tests/original/OriginalTests.csproj
dotnet test public_tests/PublicTests.csproj