#!/bin/bash
# Run all public tests with nyc coverage and mocha
npx nyc --reporter=text --reporter=html npx mocha "public_tests/**/*.js"