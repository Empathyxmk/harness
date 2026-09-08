#!/bin/bash
set -e

# Install dependencies if node_modules does not exist
if [ ! -d node_modules ]; then
  npm install
fi

# Run tests
if grep -q '"test"' package.json; then
  npm test
else
  # Fallback: run the test file(s) directly with node
  find ./test -type f -name "*.js" -exec node {} \;
fi