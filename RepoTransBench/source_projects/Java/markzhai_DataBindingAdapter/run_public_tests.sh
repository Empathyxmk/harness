#!/bin/bash
set -e

cd adapter
if [ -f "./gradlew" ]; then
    ./gradlew testDebugUnitTest --tests '*PublicTest'
else
    ./gradlew testDebugUnitTest --tests '*PublicTest'
fi
cd ..