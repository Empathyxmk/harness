#!/bin/bash
# Run all tests in the test/ directory using mocha, without nyc/coverage for simplicity and to avoid config-util error.
npx mocha "test/**/*.js"