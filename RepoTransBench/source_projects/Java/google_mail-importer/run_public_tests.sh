#!/bin/bash
# Runs only public tests using Maven's -Dtest=... option

# Find all *PublicTest.java files under src/test/java
test_classes=$(find src/test/java -name '*PublicTest.java' | sed 's|src/test/java/||' | sed 's|/|.|g' | sed 's/.java$//')
if [ -z "$test_classes" ]; then
  echo "No public test files found!"
  exit 1
fi

# Build -Dtest= pattern for Maven (comma separated)
test_classes_csv=$(echo $test_classes | tr ' ' ',')
mvn -Dtest="$test_classes_csv" test