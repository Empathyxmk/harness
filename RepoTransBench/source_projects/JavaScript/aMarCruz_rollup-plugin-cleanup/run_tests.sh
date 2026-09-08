#!/bin/bash
# Run all tests for rollup-plugin-cleanup

yarn install --frozen-lockfile

# Run jest with coverage, targeting src/
npx jest --coverage --collectCoverageFrom="src/**/*.js"