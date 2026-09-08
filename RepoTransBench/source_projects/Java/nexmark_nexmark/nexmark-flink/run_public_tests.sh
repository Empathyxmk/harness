#!/bin/bash
# Run only public tests

cd "$(dirname "$0")"

# Run only test classes with the 'PublicTest' suffix
if [ -f "./mvnw" ]; then
  ./mvnw -pl nexmark-flink test -Dtest=*PublicTest
else
  mvn -pl nexmark-flink test -Dtest=*PublicTest
fi