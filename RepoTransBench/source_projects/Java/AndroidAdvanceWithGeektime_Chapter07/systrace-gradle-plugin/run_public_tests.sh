#!/bin/bash
echo "== Running plugin PUBLIC unit tests =="
cd "$(dirname "$0")"
cd ..
chmod +x ./gradlew
./gradlew :systrace-gradle-plugin:test --tests '*PublicTest'