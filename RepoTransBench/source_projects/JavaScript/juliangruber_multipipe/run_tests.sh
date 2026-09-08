#!/bin/bash
set -e

if [ -f ./node_modules/.bin/mocha ]; then
  # run all test/*.js files via mocha
  npx mocha "test/**/*.js"
else
  if [ -d test ]; then
    for f in test/*.js; do
      node "$f"
    done
  else
    echo "No test runner or test files found."
    exit 1
  fi
fi