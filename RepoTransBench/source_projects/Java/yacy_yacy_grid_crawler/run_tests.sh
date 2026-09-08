#!/bin/bash
./gradlew clean test jacocoTestReport --no-daemon
echo "Coverage HTML: build/reports/jacoco/test/html/index.html"