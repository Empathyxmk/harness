#!/bin/bash
# Run all tests (existing/full test suite) for the project

cd "$(dirname "$0")"
./gradlew --no-daemon test