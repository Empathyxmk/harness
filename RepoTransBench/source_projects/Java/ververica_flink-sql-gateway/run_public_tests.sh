#!/bin/bash
# Run only public tests using Maven

if [ -f "./mvnw" ]; then
  ./mvnw -B -Dtest='**/*PublicTest' test
else
  mvn -B -Dtest='**/*PublicTest' test
fi