#!/bin/bash
set -e

if [ -f ./node_modules/.bin/mocha ]; then
  # run all public_tests/*.js files via plain node (not mocha, as mocha seems broken)
  for f in public_tests/*.js; do
    node "$f"
  done
else
  if [ -d public_tests ]; then
    for f in public_tests/*.js; do
      node "$f"
    done
  else
    echo "No public_test runner or test files found."
    exit 1
  fi
fi