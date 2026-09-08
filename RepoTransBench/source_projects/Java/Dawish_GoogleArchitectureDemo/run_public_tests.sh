#!/bin/bash
# Script to run all public tests in the project with proper Gradle wrapper permissions

chmod +x ./gradlew
# The public tests are in standard src/test/java/ tree but use *PublicTest.java naming. This will run all tests, including public ones.
./gradlew test --tests '*PublicTest'