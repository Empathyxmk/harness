#!/bin/bash
# Run all tests

cd "$(dirname "$0")"

if [ -f "./mvnw" ]; then
  ./mvnw -pl nexmark-flink test
else
  mvn -pl nexmark-flink test
fi