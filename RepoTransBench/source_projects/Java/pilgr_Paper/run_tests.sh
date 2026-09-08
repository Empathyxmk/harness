#!/bin/bash
set -e
cd paperdb
./gradlew clean testDebugUnitTest jacocoTestReport