#!/bin/bash
cd easygcm-lib
./gradlew clean testDebugUnitTest jacocoTestReport --no-daemon --console=plain
cd ..
echo "Tests run. See coverage in easygcm-lib/build/reports/jacoco/testDebugUnitTest/html/index.html"