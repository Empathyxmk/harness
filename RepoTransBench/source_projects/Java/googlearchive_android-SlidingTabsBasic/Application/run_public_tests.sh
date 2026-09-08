#!/bin/bash
# Run only the public tests for the project

cd "$(dirname "$0")"
./gradlew testDebugUnitTest --tests '*PublicTest' --no-daemon