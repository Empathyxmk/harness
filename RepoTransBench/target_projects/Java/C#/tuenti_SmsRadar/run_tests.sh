#!/bin/bash
set -e

dotnet build Tuenti.SmsRadar.sln
dotnet test tests/original/OriginalTests.csproj --no-build
dotnet test public_tests/PublicTests.csproj --no-build