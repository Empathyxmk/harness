#!/bin/bash
set -e

if [ ! -d "node_modules" ]; then
  npm install
fi

npx jest --coverage --coverageReporters=text --coverageReporters=html