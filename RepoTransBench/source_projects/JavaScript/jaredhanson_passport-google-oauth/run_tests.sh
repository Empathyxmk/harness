#!/bin/bash
# Run all standard (private) tests for the project
npx mocha test/package.test.js
npx mocha test/lib/index.test.js