#!/bin/bash
# Use nyc for coverage and mocha for running all test js files in test/
npx nyc --reporter=text --reporter=html npx mocha "test/**/*.js"