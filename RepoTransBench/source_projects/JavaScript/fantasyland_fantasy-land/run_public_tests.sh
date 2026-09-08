#!/bin/bash
# Run Mocha tests with NYC for coverage on public tests
npx nyc --reporter=text --reporter=html npx mocha "public_tests/**/*.js"