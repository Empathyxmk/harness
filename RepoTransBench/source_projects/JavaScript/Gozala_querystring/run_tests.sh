#!/bin/bash
set -e
# Install jest and coverage tooling if needed
if ! npx --no-install jest --version > /dev/null 2>&1; then
  npm install --no-audit --no-fund --save-dev jest
fi

export NODE_ENV=test

npx jest --coverage --coverageReporters=text --coverageReporters=html