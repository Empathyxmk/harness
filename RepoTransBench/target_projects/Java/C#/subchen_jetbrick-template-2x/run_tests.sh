#!/bin/bash
set -e

# Build and test all projects in solution
dotnet test JetbrickTemplate.sln --logger "console;verbosity=normal"