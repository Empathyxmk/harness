#!/bin/bash
# Install dependencies if node_modules is missing
if [ ! -d node_modules ]; then
  npm install --no-progress --no-audit --loglevel=error jest
fi
# Run tests with coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html