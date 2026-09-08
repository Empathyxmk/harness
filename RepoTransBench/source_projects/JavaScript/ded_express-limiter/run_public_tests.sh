#!/bin/bash
set -e

npm install

# Run coverage of only public tests with nyc and mocha
npx nyc --reporter=text --reporter=html mocha "public_tests/**/*.js"