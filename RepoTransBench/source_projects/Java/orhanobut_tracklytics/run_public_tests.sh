#!/bin/bash
# Run all public tests for orhanobut_tracklytics

# Ensure gradlew is executable
chmod +x ./gradlew

# Run only *PublicTest.java classes
./gradlew :tracklytics-runtime:test --tests '*PublicTest'

# For sample (if public tests exist in sample, add similar line)
# ./gradlew :sample:test --tests '*PublicTest'