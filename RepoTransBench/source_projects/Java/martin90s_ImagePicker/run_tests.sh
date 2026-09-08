#!/bin/bash
set -e
./gradlew :imagepicker:testDebugUnitTest jacocoTestReport
echo "HTML coverage: imagepicker/build/reports/jacoco/test/html/index.html"