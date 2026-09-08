#!/bin/bash
set -e

# Build and test only the dearbinge-openapi module with coverage report
mvn clean test jacoco:report -pl dearbinge-openapi

echo "Test and coverage report for dearbinge-openapi generated."
echo "Coverage report: dearbinge-openapi/target/site/jacoco/index.html"