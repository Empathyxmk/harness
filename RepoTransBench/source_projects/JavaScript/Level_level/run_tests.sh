#!/bin/bash
# Run tests with coverage using c8 and display text and html reports

# Remove existing coverage data if present
rm -rf coverage .nyc_output .cache .c8_marker

# Run tests with c8 -- since this is not a Jest project, use mocha as default
npx c8 --reporter=text --reporter=html npx mocha "test/**/*.js"

# Also try to cover test.js if not already included (if present and not in test/)
if [ -f test.js ]; then
  npx c8 --reporter=none node test.js
fi

# Output coverage summary again
npx c8 report --reporter=text