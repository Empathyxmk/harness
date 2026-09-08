#!/bin/bash
# Run all Feather public tests in src/test/java with code coverage, producing an HTML report

cd feather
# Only run *PublicTest.java classes, skipping originals.
mvn -Dtest=*PublicTest test jacoco:report
cd ..
echo "Coverage report for public tests available at feather/target/site/jacoco/index.html"