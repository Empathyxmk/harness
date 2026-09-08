#!/bin/bash
# Run all public tests using Mocha
if [ -f ./node_modules/.bin/mocha ]; then
  ./node_modules/.bin/mocha "public_tests/**/*.public.test.js"
else
  npx mocha "public_tests/**/*.public.test.js"
fi