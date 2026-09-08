#!/bin/bash
# Run all modules' tests using compatible Java

export JAVA_HOME="$(/usr/libexec/java_home -v 1.8)"
export PATH="$JAVA_HOME/bin:$PATH"

if [ -f ./gradlew ]; then
    ./gradlew clean test
else
    echo "Gradle wrapper not found!"
    exit 1
fi