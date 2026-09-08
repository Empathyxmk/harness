#!/bin/bash
set -e

# Clean and run Maven tests with Jacoco coverage
./mvnw clean test jacoco:report

echo "Test run completed. Coverage HTML: target/site/jacoco/index.html"