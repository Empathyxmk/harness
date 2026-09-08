#!/bin/bash
set -e

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run Jest tests with coverage
npm test