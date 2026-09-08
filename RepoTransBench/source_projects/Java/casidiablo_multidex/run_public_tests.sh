#!/bin/bash
# Use JVM flags for reflective access for Java 9+ (esp. for legacy multidex)
export JAVA_OPTS="--add-opens=java.base/java.io=ALL-UNNAMED"
# Run *PublicTest classes
./gradlew test --tests '*PublicTest' --no-daemon "$@"