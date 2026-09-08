#!/bin/bash
echo "== Running plugin unit tests =="
cd "$(dirname "$0")"
cd ..
chmod +x ./gradlew
./gradlew :systrace-gradle-plugin:test