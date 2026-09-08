#!/bin/bash
set -e

cd FitChart
./gradlew testDebugUnitTest jacocoTestReport
cd ..
echo "All tests executed. Coverage report (HTML) at FitChart/build/reports/jacoco/jacocoTestReport/html/index.html"