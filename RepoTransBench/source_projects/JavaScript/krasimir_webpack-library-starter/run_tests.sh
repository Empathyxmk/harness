#!/bin/bash
# Simple test runner for this project

if yarn test 2>/dev/null; then
  yarn test
elif npx jest --version >/dev/null 2>&1; then
  npx jest
elif npx mocha --version >/dev/null 2>&1; then
  npx mocha
elif [ -d src/__tests__ ]; then
  npx mocha "src/__tests__/*.js"
else
  echo "No test command or major test runners found."
  exit 1
fi