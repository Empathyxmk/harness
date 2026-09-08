#!/bin/bash
# Runs all test cases (existing)

cd amigo-lib

if [ -f "./gradlew" ]; then
  ./gradlew testDebugUnitTest
  ./gradlew connectedDebugAndroidTest
else
  echo "Gradle wrapper not found. Trying with system gradle..."
  gradle testDebugUnitTest
  gradle connectedDebugAndroidTest
fi

cd ..