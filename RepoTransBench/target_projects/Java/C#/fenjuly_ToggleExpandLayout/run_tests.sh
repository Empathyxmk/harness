#!/bin/bash
set -e

dotnet restore fenjuly_ToggleExpandLayout.sln

dotnet test fenjuly_ToggleExpandLayout.sln