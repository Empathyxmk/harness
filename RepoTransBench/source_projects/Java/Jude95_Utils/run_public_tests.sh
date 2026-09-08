#!/bin/bash
cd utils
./gradlew clean test --tests '*PublicTest' --no-build-cache