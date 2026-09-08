#!/bin/bash
set -e
# Clean, build, test, and create jacoco coverage report
./gradlew clean testDebugUnitTest jacocoTestReport --no-daemon
echo "Tests and code coverage run complete."
echo "HTML coverage report (if configured): app/build/reports/jacoco/test/html/index.html"