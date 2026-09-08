#!/bin/bash
# Script to run only public test cases

# Run public unit tests in both app and cmlibrary modules
./gradlew test --tests '*PublicTest*'