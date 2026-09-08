#!/bin/bash
set -e
export NODE_ENV=test

# Use Jest to run all JS tests in the root and tests/scripts/, coverage for whitelist.js
npx jest --coverage --coverageReporters=text --coverageReporters=html --testPathIgnorePatterns="node_modules"