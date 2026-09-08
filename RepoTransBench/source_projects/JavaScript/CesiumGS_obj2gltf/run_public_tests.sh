#!/bin/bash
set -e

# Run all public tests in public_tests/ using Jasmine
if [ -f "specs/jasmine.json" ]; then
  # Use the same jasmine.json but point to "public_tests"
  npx jasmine "public_tests/**/*.js"
else
  npx jasmine "public_tests/**/*.js"
fi