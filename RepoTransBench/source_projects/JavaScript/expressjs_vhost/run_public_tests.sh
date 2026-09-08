#!/bin/bash
set -e

# Install dependencies if node_modules does not exist
if [ ! -d node_modules ]; then
  npm install
fi

# Run all public tests in public_tests directory using mocha
if [ -d public_tests ]; then
  npx mocha --reporter spec --bail public_tests/
else
  echo "No public tests found"
  exit 1
fi