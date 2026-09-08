#!/bin/bash
set -e

# Install dependencies if not already installed
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run all tests using Jest for coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html