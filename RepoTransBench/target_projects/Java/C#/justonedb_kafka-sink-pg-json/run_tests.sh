#!/bin/bash
set -e

dotnet build JustOneKafkaSinkPgJson.sln
dotnet test tests/original/JustOneKafkaSinkPgJson.Tests.csproj --no-build
dotnet test public_tests/JustOneKafkaSinkPgJson.PublicTests.csproj --no-build