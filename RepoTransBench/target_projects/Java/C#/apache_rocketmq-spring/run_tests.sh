#!/bin/bash
set -e
dotnet test tests/original/RocketMQSpring.OriginalTests.csproj
dotnet test public_tests/RocketMQSpring.PublicTests.csproj