#!/bin/bash
set -e

cd channelview
./gradlew clean testDebugUnitTest jacocoTestReport --no-daemon
cd ..