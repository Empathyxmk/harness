#!/bin/bash
echo "== Running app PUBLIC instrumented tests =="
cd "$(dirname "$0")"
cd ../..
chmod +x ./gradlew
./gradlew :systrace-sample-android:app:testDebugUnitTest --tests '*PublicTest'