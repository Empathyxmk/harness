#!/bin/bash
# Clean simple test runner with NYC and Mocha

export NODE_ENV=test

# Only run tests in ./test (avoiding potential issues with node_modules test files)
npx nyc --reporter=html --reporter=text npx mocha --require test/bootstrap/node.js "test/**/*.test.js"