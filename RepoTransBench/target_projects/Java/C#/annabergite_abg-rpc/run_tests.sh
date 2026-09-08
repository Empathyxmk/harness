#!/bin/bash
set -e
dotnet test tests/original/AnnabergiteAbgRpc.OriginalTests.csproj
dotnet test public_tests/AnnabergiteAbgRpc.PublicTests.csproj