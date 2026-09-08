#!/bin/bash
set -e

npm install

# Run mocha with nyc for test coverage
npx nyc --reporter=text --reporter=html npx mocha test.js

echo "All tests passed."