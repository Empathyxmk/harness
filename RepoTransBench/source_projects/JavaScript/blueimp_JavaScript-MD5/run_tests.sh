#!/bin/bash
set -e
npm install
npx nyc --reporter=text --reporter=html mocha "test/**/*.test.js"