#!/bin/bash
# Run all existing Java/JUnit tests for fafaldo-zz_FABToolbar

cd "$(dirname "$0")"

# Run JVM unit tests (default)
./gradlew :library:test

# Run Android instrumentation tests
./gradlew :app:connectedAndroidTest
./gradlew :library:connectedAndroidTest