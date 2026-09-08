#!/bin/bash
set -e

echo "Testing multi-release-jar..."
cd multi-release-jar
mvn clean test jacoco:report
cd ..

echo "Testing java15/nashorn_fixed..."
cd java15/nashorn_fixed
mvn clean test jacoco:report
cd ../..

echo "Testing java15/nashorn_broken..."
cd java15/nashorn_broken
mvn clean test jacoco:report
cd ../..