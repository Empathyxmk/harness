#!/bin/bash
# Compile and run PUBLIC tests in src/test/java
set -e
mkdir -p target/public-test-classes

# Java 11 to guarantee compatibility with older JDKs (class version 55.0)
JAVA_VERSION=11

echo "Downloading JUnit 4.13.2 and Hamcrest Core 1.3 if needed..."
[ -f junit-4.13.2.jar ] || wget -q https://repo1.maven.org/maven2/junit/junit/4.13.2/junit-4.13.2.jar
[ -f hamcrest-core-1.3.jar ] || wget -q https://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar

echo "Compiling and running PUBLIC tests with javac & JUnit..."

find src/test/java -name "*PublicTest.java" > .sources_public_tests.txt

javac -source $JAVA_VERSION -target $JAVA_VERSION -cp "junit-4.13.2.jar:hamcrest-core-1.3.jar:src/main/java" \
  -d target/public-test-classes @.sources_public_tests.txt

java -cp "target/public-test-classes:src/main/java:junit-4.13.2.jar:hamcrest-core-1.3.jar" \
  org.junit.runner.JUnitCore com.commonsguy.cwac.merge.MergeAdapterPublicTest