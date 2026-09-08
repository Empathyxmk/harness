#!/bin/bash
# Run all public tests in the public_tests directory using mocha
export NODE_ENV=test
if [ -d ./public_tests ]; then
  npx mocha "./public_tests/**/*.public.test.js"
else
  echo "No public_tests directory found."
  exit 1
fi
chmod +x ./public_tests/run_public_tests.sh