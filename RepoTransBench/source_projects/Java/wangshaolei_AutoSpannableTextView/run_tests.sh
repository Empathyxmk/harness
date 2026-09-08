#!/bin/bash
# Run all existing tests using Gradle
./gradlew clean test
./gradlew :app:assembleDebug
./gradlew :app:connectedAndroidTest