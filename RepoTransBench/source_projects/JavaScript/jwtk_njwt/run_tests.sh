#!/bin/bash
set -e

# Run all test files in the test directory using mocha (default test script)
if [ -f "node_modules/.bin/mocha" ]; then
  npx mocha test/*.js
else
  if npm run | grep -q "test"; then
    npm test
  else
    echo "Mocha is not installed and no test script found in package.json"
    exit 1
  fi
fi