#!/bin/bash
set -e

# Run nyc with mocha to collect coverage
npx nyc --reporter=text --reporter=html ./node_modules/mocha/bin/mocha "test/**/*.js"