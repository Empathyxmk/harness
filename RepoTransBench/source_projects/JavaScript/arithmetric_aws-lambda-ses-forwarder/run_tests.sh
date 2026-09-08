#!/bin/bash
set -e

# Install dependencies if not already present
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run all tests with coverage
npm run coverage