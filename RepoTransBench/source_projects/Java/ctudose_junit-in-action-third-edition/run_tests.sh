#!/bin/bash

# Define the base directory for the project
BASE_DIR=$(pwd)

# Define the module to focus on for this iteration
MODULE_DIR="ch02-core"

echo "Running tests and generating coverage for $MODULE_DIR..."

# Navigate to the module directory, run Maven goals, and then navigate back
(cd "$MODULE_DIR" && mvn clean verify jacoco:report)

echo "Coverage report generated in $MODULE_DIR/target/site/jacoco/index.html"