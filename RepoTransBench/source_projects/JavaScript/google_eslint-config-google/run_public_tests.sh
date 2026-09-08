#!/bin/bash
set -e

# Install dependencies if not already installed
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run all public tests using Jest
npx jest public_tests/ --coverage=false