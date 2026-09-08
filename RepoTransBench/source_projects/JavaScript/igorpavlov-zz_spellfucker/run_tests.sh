#!/bin/bash
set -e

export NODE_ENV=test

# Run jest tests and collect coverage using nyc
npx nyc --reporter=lcov --reporter=text npx jest --runInBand