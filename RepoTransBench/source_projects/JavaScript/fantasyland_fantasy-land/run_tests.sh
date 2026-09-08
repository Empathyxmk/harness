#!/bin/bash
# Run Mocha tests with NYC for coverage
npx nyc --reporter=text --reporter=html npx mocha "test/**/*.js"