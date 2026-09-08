#!/bin/bash
# Install dependencies if not already present
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run jest with coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html