#!/bin/bash
set -e

echo "-------------------------------------------"
echo "Running Jest unit tests with coverage ..."
echo "-------------------------------------------"

npx jest --coverage --coverageReporters=text --coverageReporters=html

echo "-------------------------------------------"
echo "All tests (if any) executed."
echo "-------------------------------------------"