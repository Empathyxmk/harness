#!/bin/bash
set -e

npm install

# Always run coverage with nyc and mocha on all test files
npx nyc --reporter=text --reporter=html mocha "tests/**/*.js"