#!/bin/bash

# Define the base directory for the project
BASE_DIR=$(pwd)

# Define the module to focus on for this iteration
MODULE_DIR="ch02-core"

echo "Running PUBLIC tests for $MODULE_DIR..."

# Run only public tests by specifying includes. We target *PublicTest.java.
(cd "$MODULE_DIR" && mvn -Dtest=*PublicTest test)

echo "All public tests finished in $MODULE_DIR"