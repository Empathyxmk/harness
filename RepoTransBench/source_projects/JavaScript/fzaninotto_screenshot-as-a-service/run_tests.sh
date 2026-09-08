#!/bin/bash
# Install dependencies if not yet installed
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run tests with coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html