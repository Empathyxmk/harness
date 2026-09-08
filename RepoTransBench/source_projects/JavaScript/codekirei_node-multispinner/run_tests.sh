#!/bin/bash
set -e

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  npm install
fi

# Use jest for running tests with coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html