#!/bin/bash
set -e

echo "Running PUBLIC Jest test suite..."

npx jest public_tests/ --runInBand --testTimeout=20000

echo "Public test suite complete."