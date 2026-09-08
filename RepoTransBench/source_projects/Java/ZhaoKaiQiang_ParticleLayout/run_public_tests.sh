#!/bin/bash
set -e
# Run all public test files for all modules using Maven or Gradle if available
if [ -f "./mvnw" ]; then
  ./mvnw test -Dtest=*PublicTest
elif [ -f "./gradlew" ]; then
  ./gradlew test --tests "*PublicTest"
elif [ -f "Leonids/gradlew" ]; then
  cd Leonids
  ./gradlew test --tests "*PublicTest"
  cd ..
else
  # Try calling gradle directly if it's installed globally
  gradle :Leonids:test --tests "*PublicTest"
  gradle :app:test --tests "*PublicTest"
  gradle :library:test --tests "*PublicTest"
fi