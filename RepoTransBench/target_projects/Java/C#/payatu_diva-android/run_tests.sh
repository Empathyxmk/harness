#!/bin/bash
set -e

# Build the solution and run all tests (original and public)
dotnet test PayatuDivaAndroid.sln --no-build --logger "console;verbosity=normal" || dotnet test PayatuDivaAndroid.sln --logger "console;verbosity=normal"