#!/bin/bash
set -e
dotnet restore
dotnet test Vatri.Ecommerce.sln --no-build