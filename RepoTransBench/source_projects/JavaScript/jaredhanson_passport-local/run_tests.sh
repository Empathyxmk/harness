#!/bin/bash
# Load test bootstrap files if present then run all test/*.test.js using mocha
if [ -f ./test/bootstrap/node.js ]; then
  NODE_ENV=test node -r ./test/bootstrap/node.js ./node_modules/mocha/bin/mocha --recursive test/*.test.js
else
  NODE_ENV=test ./node_modules/mocha/bin/mocha --recursive test/*.test.js
fi