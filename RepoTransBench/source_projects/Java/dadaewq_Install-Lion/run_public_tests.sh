#!/bin/bash
set -e

echo "Running Maven build and PUBLIC tests only..."
mvn -Dtest=CalculatorPublicTest test

echo "Public tests completed successfully."