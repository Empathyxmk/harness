#!/bin/bash
# Run all tests for the payload_reader module

cd "$(dirname "$0")"

chmod +x ./gradlew
./gradlew test