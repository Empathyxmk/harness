#!/bin/bash
set -e

npm install

if npx --no-install mocha --version > /dev/null 2>&1; then
  npx mocha test_public/*.public.test.js
elif npx --no-install tape --version > /dev/null 2>&1; then
  npx tape test_public/*.public.test.js
else
  if npm run | grep -q 'test'; then
    npm test test_public/*.public.test.js
  else
    echo "No appropriate test runner found for public tests."
    exit 1
  fi
fi