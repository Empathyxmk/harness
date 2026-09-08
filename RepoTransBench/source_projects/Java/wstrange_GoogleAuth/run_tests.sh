#!/bin/bash
# Run tests with coverage using Maven and output results to console and HTML

mvn clean test jacoco:report
EXIT_CODE=$?
echo "HTML Coverage Report: target/site/jacoco/index.html"
exit $EXIT_CODE