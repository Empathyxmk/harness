#!/bin/bash
# Install dependencies if node_modules is missing
if [ ! -d node_modules ]; then
  npm install --no-progress --no-audit --loglevel=error jest
fi
# Run only the public tests
npx jest public_tests/ --coverage=false