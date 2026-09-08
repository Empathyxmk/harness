#!/bin/bash
set -e
dotnet restore
dotnet test inloop_easygcm.sln --logger "console;verbosity=detailed"