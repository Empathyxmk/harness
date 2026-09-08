#!/bin/bash
echo "== Running all PUBLIC module/standard & instrumentation tests =="
./gradlew clean test --tests '*PublicTest'
./gradlew :systrace-sample-android:app:connectedAndroidTest -PpublicTestsOnly=true