#!/bin/bash
# Public test runner
export NODE_ENV=test
npx nyc --reporter=html --reporter=text npx mocha --require test/bootstrap/node.js "test_public/**/*.public.test.js"