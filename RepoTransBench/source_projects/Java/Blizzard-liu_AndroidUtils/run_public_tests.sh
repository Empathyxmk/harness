#!/bin/bash
# Script to run only public test cases (those ending with PublicTest) for ALL modules using gradle
set -e
./gradlew clean test --tests '*PublicTest'