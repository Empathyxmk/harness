#!/bin/bash
# Run all original test suites

echo "Running stemer_vows.js"
node test/stemer_vows.js

echo "    Running memoizing_stemmer_vows.js"
node test/memoizing_stemmer_vows.js

echo "    Running mocha-based tests"
npx mocha --require test/index.js "test/porter.spec.js"
npx mocha --require test/index.js "test/porter-branches.spec.js"