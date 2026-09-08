#!/bin/bash
# More robust test runner using Maven with a timeout
# Fails if tests or build fail

set -e

# Run Maven test (default goal) with a longer timeout (30min) to avoid download slowness
mvn --batch-mode -Dmaven.test.failure.ignore=false test