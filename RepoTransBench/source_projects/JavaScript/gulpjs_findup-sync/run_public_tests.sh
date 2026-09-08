#!/bin/bash
set -e

# Run ONLY the public tests (those in the public_tests folder)
npx mocha "public_tests/**/*.js"