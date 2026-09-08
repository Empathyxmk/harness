#!/bin/bash
set -e

# Install dependencies if node_modules does not exist
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run coverage with jest
npx jest --coverage --coverageReporters=text --coverageReporters=html