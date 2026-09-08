#!/bin/bash
cd lib_round
./gradlew clean testDebugUnitTest jacocoTestReport
cd ..
echo "Open coverage summary at: lib_round/build/reports/jacoco/test/html/index.html"