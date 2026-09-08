#!/bin/bash
set -e

cd preferenceroom-compiler
./gradlew clean test --tests "*PublicTest"
cd ..

cd demo
./gradlew clean connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.skydoves.preferenceroomdemo.components.AppComponentPublicTest
./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.skydoves.preferenceroomdemo.components.JunitComponentPublicTest
./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.skydoves.preferenceroomdemo.entities.ProfileEntityPublicTest
./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.skydoves.preferenceroomdemo.entities.DeviceEntityPublicTest
cd ..