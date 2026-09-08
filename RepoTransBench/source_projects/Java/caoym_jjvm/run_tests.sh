#!/bin/bash
set -e
echo "Running tests with coverage..."

mvn clean test jacoco:report

REPORT=target/site/jacoco/index.html
if test -f "$REPORT"; then
  echo "Coverage report generated: $REPORT"
else
  echo "Coverage report not found!"
fi