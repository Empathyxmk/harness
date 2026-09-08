#!/bin/bash
# Use Java 8 for Gradle compatibility if present, else fallback
if type -p java; then
    JAVA_VER=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    case "$JAVA_VER" in
      1.8*|8*) export JAVA_HOME=$(/usr/libexec/java_home -v1.8 2>/dev/null || true) ;;
    esac
fi
# Run all tests, including unit and instrumentation
./gradlew clean testDebugUnitTest connectedDebugAndroidTest