#!/bin/bash
set -e

echo "Running Composite tests with coverage reporting..."
cd composite
mvn clean test jacoco:report
cd ..

echo "All tests completed."