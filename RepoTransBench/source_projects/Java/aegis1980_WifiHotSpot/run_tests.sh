#!/bin/bash
# Run all tests for the aegis1980_WifiHotSpot project using Maven

set -e

mvn clean test jacoco:report

if [ -f target/site/jacoco/index.html ]; then
  echo "Coverage report generated at target/site/jacoco/index.html"
else
  echo "Coverage report was NOT generated."
  exit 1
fi