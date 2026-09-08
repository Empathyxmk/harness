#!/bin/bash
set -e

echo "Running PUBLIC Jest tests..."
npx jest public_tests/ --ci