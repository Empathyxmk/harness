#!/bin/bash
# Script to run all public (PublicTest) unit and instrumented tests

set -e

# Run public unit tests
./gradlew testDebugUnitTest --tests '*PublicTest'

# Run public instrumented tests (if present)
./gradlew connectedAndroidTest --tests '*PublicTest'