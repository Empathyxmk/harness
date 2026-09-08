#!/bin/bash
# Run public tests for the project

cd "$(dirname "$0")"
./gradlew --no-daemon test --tests '*PublicTest'