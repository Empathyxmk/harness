#!/bin/bash
set -e

# Run public test suite
npx mocha "public_tests/**/*.js"