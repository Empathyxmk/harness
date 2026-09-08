#!/bin/bash
# Runs only public test classes using Maven's -Dtest=... parameter

# List all *PublicTest.java classes in src/test/java
PUBLIC_TEST_CLASSES=$(find src/test/java -type f -name '*PublicTest.java' | sed 's@src/test/java/@@; s@/@.@g; s/.java$//')

if [ -z "$PUBLIC_TEST_CLASSES" ]; then
  echo "No public tests found."
  exit 1
fi

# Join class names with commas
CLASSLIST=$(echo $PUBLIC_TEST_CLASSES | tr ' ' ',')

echo "Running public test classes:"
echo "$PUBLIC_TEST_CLASSES"
mvn -Dtest="$CLASSLIST" test