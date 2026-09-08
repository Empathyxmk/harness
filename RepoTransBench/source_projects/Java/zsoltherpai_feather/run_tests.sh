#!/bin/bash
# Run all feather unit tests with code coverage, producing an HTML report

cd feather
mvn test jacoco:report
cd ..
echo "Coverage report available at feather/target/site/jacoco/index.html"