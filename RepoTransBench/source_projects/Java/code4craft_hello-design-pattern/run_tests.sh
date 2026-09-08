#!/bin/bash
set -e

# Compile and run tests with coverage (including source/target for Java 1.7)
mvn test jacoco:report -Dmaven.compiler.source=1.7 -Dmaven.compiler.target=1.7

# Show location of JaCoCo report for convenience
echo "Coverage HTML Report available at: target/site/jacoco/index.html"