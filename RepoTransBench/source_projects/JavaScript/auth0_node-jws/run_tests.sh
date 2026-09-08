#!/bin/bash
set -e

npm install

# If there is an npm test script, use it; otherwise, run mocha directly if installed
if npm run | grep -q 'test'; then
  npm test
else
  if npx --no-install mocha --version > /dev/null 2>&1; then
    npx mocha
  else
    echo "No test runner found. Please add a test script to package.json or install mocha."
    exit 1
  fi
fi