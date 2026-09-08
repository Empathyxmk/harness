#!/bin/bash
set -e

# Install dependencies if node_modules does not exist
if [ ! -d "node_modules" ]; then
    npm install
fi

# Use jest --coverage for proper test run and reporting
npx jest --coverage --coverageReporters=text --coverageReporters=html