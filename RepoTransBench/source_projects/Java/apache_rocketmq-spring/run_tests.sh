#!/bin/bash
set -e

# Run tests and coverage in all sample and main modules with relevant source/tests
mvn -B clean test jacoco:report

# Print where the main report lives (for Maven, in target/site/jacoco/)
echo "JaCoCo HTML report available in ./target/site/jacoco/index.html"