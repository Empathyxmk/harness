#!/bin/bash
set -e

# Restore packages, build, and run all tests in the solution.
dotnet test ProjectName.sln --no-build --verbosity normal || {
  # If bin/obj don't exist yet, do a build first
  dotnet build ProjectName.sln --configuration Debug
  dotnet test ProjectName.sln --no-build --verbosity normal
}