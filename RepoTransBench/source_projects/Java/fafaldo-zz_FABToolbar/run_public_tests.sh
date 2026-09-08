#!/bin/bash
# Run all public test cases for fafaldo-zz_FABToolbar

cd FABToolbar

# Run ONLY the JVM unit tests that are named *PublicTest
./gradlew :library:test --tests "*PublicTest"

# Run public Android instrumentation tests (use test class selector via -Pandroid.testInstrumentationRunnerArguments.class)
./gradlew :app:connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.github.fafaldo.fabtoolbar.ApplicationPublicTest
./gradlew :library:connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.github.fafaldo.fabtoolbar.ApplicationPublicTest