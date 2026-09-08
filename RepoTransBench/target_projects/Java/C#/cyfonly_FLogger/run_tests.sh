#!/bin/bash
set -e

# Build all projects (main, test), restore dependencies.
dotnet restore

# Run all tests (original + public)
dotnet test tests/original/cyfonly_FLogger.Tests.Original.csproj
dotnet test public_tests/cyfonly_FLogger.Tests.Public.csproj