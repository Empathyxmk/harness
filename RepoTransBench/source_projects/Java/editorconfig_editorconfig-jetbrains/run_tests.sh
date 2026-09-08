#!/bin/bash
set -e
# Compile and run tests with coverage, output JaCoCo HTML report
if [ -f "pom.xml" ]; then
    mvn test jacoco:report
elif [ -f "build.gradle" ]; then
    ./gradlew test jacocoTestReport
else
    # Fallback: use junit-platform-console-standalone if no build tools
    mkdir -p out/test
    javac -cp "src/test/java:src/main/java:src:$(find ~/.m2/repository/org/junit/platform/junit-platform-console-standalone -name '*.jar' | head -n1)" \
        -d out/test \
        $(find src/main/java -name "*.java") \
        $(find src/test/java -name "*.java")
    java -jar $(find ~/.m2/repository/org/junit/platform/junit-platform-console-standalone -name '*.jar' | head -n1) \
        --class-path out/test \
        --scan-class-path
fi