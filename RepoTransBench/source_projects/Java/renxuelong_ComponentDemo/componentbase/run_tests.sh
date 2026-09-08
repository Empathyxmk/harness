#!/bin/bash
set -e

./gradlew :componentbase:testDebugUnitTest
./gradlew :componentbase:jacocoTestReport

echo "HTML coverage report generated at: componentbase/build/reports/jacoco/jacocoTestReport/html/index.html"