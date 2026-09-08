#!/bin/bash
# Script to run all existing tests

# Ensure gradlew is executable
chmod +x ./gradlew

# Run tests (all, including normal and test source sets)
./gradlew test