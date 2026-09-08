#!/bin/bash
set -e
# Run all unit and instrumentation tests for all modules using Maven if available, or Gradle wrapper if present
if [ -f "./mvnw" ]; then
  ./mvnw test
elif [ -f "./gradlew" ]; then
  ./gradlew test
elif [ -f "Leonids/gradlew" ]; then
  cd Leonids
  ./gradlew test
  cd ..
else
  # Try calling gradle directly if it's installed globally
  gradle :Leonids:test
  gradle :app:test
  gradle :library:test
fi