#!/bin/bash
set -e
cd Studio/GridListViewAdapters/gridlistviewadapters
./gradlew clean test jacocoTestReport --no-daemon