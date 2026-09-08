#!/bin/bash
set -e
echo "Running tests with coverage..."
mvn -B test jacoco:report