#!/bin/bash
set -e
cd Studio/GridListViewAdapters/gridlistviewadapters
./gradlew clean test --tests '*PublicTest' --no-daemon