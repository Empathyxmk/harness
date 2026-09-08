#!/bin/bash
# Run all public tests (public_tests/*.public.test.js) with the same bootstrap as core tests
if [ -f ./test/bootstrap/node.js ]; then
  NODE_ENV=test node -r ./test/bootstrap/node.js ./node_modules/mocha/bin/mocha --recursive public_tests/*.public.test.js
else
  NODE_ENV=test ./node_modules/mocha/bin/mocha --recursive public_tests/*.public.test.js
fi