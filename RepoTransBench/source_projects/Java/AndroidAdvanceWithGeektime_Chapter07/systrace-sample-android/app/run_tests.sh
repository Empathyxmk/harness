#!/bin/bash
echo "== Running app instrumented tests =="
cd "$(dirname "$0")"
cd ../..
chmod +x ./gradlew
./gradlew :systrace-sample-android:app:testDebugUnitTest