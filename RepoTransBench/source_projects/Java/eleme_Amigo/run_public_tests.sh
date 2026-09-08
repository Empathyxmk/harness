#!/bin/bash
# Runs public test cases only

cd amigo-lib

# Only include *PublicTest.java JUnit or instrumentation tests
# Use testDebugUnitTest for unit tests, connectedDebugAndroidTest for Android instrumented
if [ -f "./gradlew" ]; then
  ./gradlew testDebugUnitTest --tests "*PublicTest"
  ./gradlew connectedDebugAndroidTest --tests "*PublicTest"
else
  echo "Gradle wrapper not found. Trying with system gradle..."
  gradle testDebugUnitTest --tests "*PublicTest"
  gradle connectedDebugAndroidTest --tests "*PublicTest"
fi

cd ..