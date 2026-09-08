#!/bin/bash
set -e

echo "Ensuring Maven is installed..."
if ! command -v mvn &> /dev/null
then
    echo "Maven not found. Installing..."
    apt-get update && apt-get install -y maven
fi

if [ -f pom.xml ]; then
  echo "Running ONLY public tests in KafkaServicePublicTest.java"
  # Prevent surefire from running KafkaServiceTest by only specifying *PublicTest
  mvn -Dtest=KafkaServicePublicTest test
else
  echo "No pom.xml found in the root directory. Cannot run Maven tests."
  exit 1
fi