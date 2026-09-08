#!/bin/bash
# Run all public tests in public_tests/ with mocha and c8 coverage (for consistency)
npx c8 --reporter=text --reporter=html npx mocha "public_tests/**/*.js"