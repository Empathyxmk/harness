#!/bin/bash
set -e

# Run full test suite with coverage
npx nyc --reporter=text --reporter=html npx mocha "test/**/*.js"