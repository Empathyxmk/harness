#!/bin/bash
echo "== Running all module/standard & instrumentation tests =="
./gradlew clean test
./gradlew :systrace-sample-android:app:connectedAndroidTest