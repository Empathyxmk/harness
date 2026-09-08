#!/bin/bash
# Run all public tests using Gradle, filtering by *PublicTest.java files

# Unit public tests
./gradlew test --tests '*PublicTest'

# Android instrumentation public tests (if any)
./gradlew :app:assembleDebug
./gradlew :app:connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.len.ApplicationPublicTest