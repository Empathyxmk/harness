#!/bin/bash
set -e

# Simple test runner for all Java (JUnit) tests.
# Requires Maven installed.
echo "Running all Java tests (JUnit, both original and public)..."
mvn clean test
echo "Tests finished."