#!/bin/bash
set -e

# Runs all public tests in the public_tests directory, if any exist.
if [ -d "./public_tests" ] && [ "$(ls -A ./public_tests/*.js 2>/dev/null)" ]; then
  if [ -f "node_modules/.bin/mocha" ]; then
    npx mocha public_tests/*.js
  else
    echo "Mocha is not installed. Please run 'npm install' first."
    exit 1
  fi
else
  echo "No public test files found in ./public_tests"
fi