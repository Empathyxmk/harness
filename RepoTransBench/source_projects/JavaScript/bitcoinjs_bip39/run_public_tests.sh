#!/bin/bash
# Run all public tests (use --runTestsByPath for Jest, or via pattern as needed)

set -e

if grep -q "tsc" package.json 2>/dev/null; then
  if npx --no -- tsc --version &>/dev/null; then
    npx tsc --noEmit
  elif npx --no -- typescript --version &>/dev/null; then
    npx typescript --noEmit
  fi
elif [ -f tsconfig.json ]; then
  if npx --no -- tsc --version &>/dev/null; then
    npx tsc --noEmit
  fi
fi

if grep -q "jest" package.json 2>/dev/null; then
  npx jest --colors public_tests
elif grep -q "mocha" package.json 2>/dev/null; then
  npx mocha "public_tests/**/*.js"
else
  echo "No recognized test runner" >&2
  exit 1
fi