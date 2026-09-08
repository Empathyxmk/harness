#!/bin/bash
set -e

# Use local mocha binary directly for compatibility with nyc
npx nyc --reporter=text --reporter=html ./node_modules/mocha/bin/mocha test/*.js

echo "All tests passed with coverage!"