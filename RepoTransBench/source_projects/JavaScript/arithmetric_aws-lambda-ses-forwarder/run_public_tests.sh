#!/bin/bash
set -e

# Install dependencies if not already present
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run only public tests in ./public_tests
npx jest public_tests --passWithNoTests