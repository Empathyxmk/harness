#!/bin/bash
set -e

# Run the test suite with the most likely test runner
# Check if there is a test script in package.json, otherwise default to node test/index.js

if npm run | grep -q "^  test"; then
  npm test
else
  node test/index.js
fi