#!/bin/bash
# Runs only *PublicTest classes (both instrumentation and unit)
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/paperdb"

echo "Running public unit tests..."
./gradlew testDebugUnitTest --tests '*PublicTest'

echo "Running public instrumentation (androidTest) tests..."
./gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=io.paperdb.DataPublicTest
./gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=io.paperdb.CustomBookPublicTest
./gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=io.paperdb.PaperPublicTest

cd "$DIR"
echo "All public tests completed."