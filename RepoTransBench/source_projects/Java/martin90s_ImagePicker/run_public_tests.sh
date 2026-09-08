#!/bin/bash
set -e
./gradlew :imagepicker:testDebugUnitTest --tests '*PublicTest'
echo "HTML coverage: imagepicker/build/reports/jacoco/test/html/index.html"