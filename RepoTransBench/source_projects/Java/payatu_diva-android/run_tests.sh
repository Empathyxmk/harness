#!/bin/bash
# Use Java 8 for Gradle/Android test suite if java 17 is not supported
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
./gradlew test --no-daemon