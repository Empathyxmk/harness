#!/bin/bash
# Run public tests with coverage using c8 and display text and html reports

# Remove existing coverage data if present
rm -rf coverage .nyc_output .cache .c8_marker

# Run public tests with c8
npx c8 --reporter=text --reporter=html npx mocha "public_tests/**/*.js"

# Output coverage summary
npx c8 report --reporter=text