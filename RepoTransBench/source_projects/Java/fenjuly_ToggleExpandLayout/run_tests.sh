#!/bin/bash
cd library

# Run unit tests and generate jacoco test coverage
../gradlew clean testDebugUnitTest jacocoTestReport

echo "=== Jacoco HTML report at: library/build/reports/jacoco/jacocoTestReport/html/index.html ==="