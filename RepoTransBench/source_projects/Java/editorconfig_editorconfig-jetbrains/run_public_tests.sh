#!/bin/bash
set -e
# Compile and run only public tests (UtilsPublicTest)
if [ -f "pom.xml" ]; then
    mvn -Dtest=org.editorconfig.UtilsPublicTest test
elif [ -f "build.gradle" ]; then
    ./gradlew test --tests "org.editorconfig.UtilsPublicTest"
else
    # Fallback: use junit-platform-console-standalone for only public test
    mkdir -p out/publictest
    javac -cp "src/test/java:src/main/java:src:$(find ~/.m2/repository/org/junit/platform/junit-platform-console-standalone -name '*.jar' | head -n1)" \
        -d out/publictest \
        $(find src/main/java -name "*.java") \
        src/test/java/org/editorconfig/UtilsPublicTest.java
    java -jar $(find ~/.m2/repository/org/junit/platform/junit-platform-console-standalone -name '*.jar' | head -n1) \
        --class-path out/publictest \
        --select-class org.editorconfig.UtilsPublicTest
fi