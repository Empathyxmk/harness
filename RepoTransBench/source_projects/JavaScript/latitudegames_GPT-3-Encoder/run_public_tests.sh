#!/bin/bash
set -e

# Install dependencies if node_modules does not exist
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run public tests only
npx jest public_tests/ --coverage=false