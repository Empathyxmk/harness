#!/bin/bash
set -e

# Run Mocha tests with coverage using NYC
npx nyc --reporter=text --reporter=html mocha "test/**/*.js"