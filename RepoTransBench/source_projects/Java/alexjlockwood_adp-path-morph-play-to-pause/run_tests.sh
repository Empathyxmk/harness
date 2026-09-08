#!/bin/bash
set -e

echo "Running tests and generating coverage report..."
mvn test jacoco:report

report="target/site/jacoco/index.html"
if [ -f "$report" ]; then
  echo "JaCoCo report generated at $report"
else
  echo "JaCoCo report not found"
fi