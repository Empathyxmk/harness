#!/bin/bash
# Script to run all tests and generate coverage

# Use Maven to run tests with JaCoCo coverage report
mvn clean test jacoco:report

# Output result status
if [ $? -eq 0 ]; then
  echo "Tests ran successfully."
else
  echo "Test failure or error."
  exit 1
fi