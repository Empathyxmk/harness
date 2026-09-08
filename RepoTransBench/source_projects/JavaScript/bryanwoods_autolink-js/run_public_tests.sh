#!/bin/bash
# Run only public tests in public_tests/ directory
if [ ! -d "node_modules" ]; then
  npm install
fi

npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html