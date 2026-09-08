#!/bin/bash
set -e
cd Application
./gradlew clean testDebugUnitTest jacocoTestReport --no-daemon
echo "Coverage report output at: Application/build/reports/jacoco/testDebugUnitTest/html/index.html"