#!/bin/bash
# Run all existing Java/JUnit and Android instrumentation tests for fafaldo-zz_FABToolbar

cd FABToolbar

# Run JVM unit tests (library module)
./gradlew :library:test

# Run Android instrumentation tests (app and library modules)
./gradlew :app:connectedAndroidTest
./gradlew :library:connectedAndroidTest