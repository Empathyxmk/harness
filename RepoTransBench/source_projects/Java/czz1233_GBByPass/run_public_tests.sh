#!/bin/bash
set -e
echo "Running PUBLIC tests with coverage..."
mvn -B -Dtest='*PublicTest' test jacoco:report