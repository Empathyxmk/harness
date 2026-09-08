#!/bin/bash
set -e

echo "== Building solution =="
dotnet build --nologo

echo
echo "== Running all tests (original + public) =="
dotnet test --no-build --nologo --verbosity normal