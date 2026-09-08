#!/bin/bash
set -e

echo "Testing multi-release-jar public tests..."
cd multi-release-jar
mvn -Dtest=StudentPublicTest,ApplicationPublicTest test
if [ -d src/test/java17/com/example ]; then
    mvn -Dtest=com.example.StudentPublicTest test -f pom.xml
fi
cd ..

echo "Testing java15/nashorn_fixed public tests..."
cd java15/nashorn_fixed
mvn -Dtest=NashornExamplePublicTest test
cd ../..

echo "Testing java15/nashorn_broken public tests..."
cd java15/nashorn_broken
mvn -Dtest=NashornExamplePublicTest test
cd ../..

echo "Testing java11/removed_fonts public tests..."
cd java11/removed_fonts
mvn -Dtest=FontExamplePublicTest test
cd ../../..