#!/bin/bash
set -e

echo "Running Maven build and tests with JaCoCo coverage..."
mvn clean test jacoco:report

echo "Coverage HTML report available at: target/site/jacoco/index.html"