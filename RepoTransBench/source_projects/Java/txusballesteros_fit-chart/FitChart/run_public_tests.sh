#!/bin/bash
cd "$(dirname "$0")"
./gradlew test --tests '*PublicTest'