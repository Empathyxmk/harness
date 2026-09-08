#!/bin/bash
# Run all public tests for rollup-plugin-cleanup

yarn install --frozen-lockfile

# Run only the public tests in public_tests/
npx jest --coverage=false public_tests/