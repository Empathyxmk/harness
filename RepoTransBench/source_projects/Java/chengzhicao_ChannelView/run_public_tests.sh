#!/bin/bash
set -e

echo "[INFO] Running public tests for app..."
cd app
./gradlew clean testDebugUnitTest --tests '*PublicTest' --no-daemon
cd ..

echo "[INFO] Running public tests for channelview..."
cd channelview
./gradlew clean testDebugUnitTest --tests '*PublicTest' --no-daemon
cd ..