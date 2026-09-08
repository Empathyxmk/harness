#!/bin/bash
set -e

# Install dependencies if node_modules is missing
if [ ! -d "node_modules" ]; then
  npm install
fi

npx jest --coverage --coverageReporters=text --coverageReporters=html