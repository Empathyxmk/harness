#!/bin/bash
set -e

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  npm install
fi

# Run only public tests (those in public_tests/)
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html