#!/bin/bash
set -e

# Only run JS public tests (omit existing/A/B/cs/etc. tests)
npx nyc --reporter=text --reporter=html npx mocha "public_tests/**/*.js"