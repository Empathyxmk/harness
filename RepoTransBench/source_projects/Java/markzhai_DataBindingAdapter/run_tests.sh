#!/bin/bash
set -e

cd adapter
if [ -f "./gradlew" ]; then
    ./gradlew testDebugUnitTest jacocoTestReport
else
    ./gradlew testDebugUnitTest jacocoTestReport
fi
cd ..