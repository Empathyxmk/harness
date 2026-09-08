#!/bin/bash
# Run all (existing) tests for the comet module
cd "$(dirname "$0")"
if [ -x ./mvnw ]; then
  ./mvnw -B test
else
  mvn -B test
fi