#!/bin/bash
# Run only public test classes for YaCy Grid Crawler

# Clean and test only public test classes (using gradle's --tests inclusion filter)
./gradlew clean test --tests '*PublicTest' --no-daemon
echo "Public test coverage HTML: build/reports/jacoco/test/html/index.html"