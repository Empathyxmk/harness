#!/bin/bash
set -e
./gradlew :tracklytics-runtime:test :tracklytics-runtime:jacocoTestReport --no-daemon