#!/bin/bash
set -e

# Measure coverage using jest
if [ -x ./node_modules/.bin/jest ]; then
  ./node_modules/.bin/jest --coverage --coverageReporters=text --coverageReporters=html
else
  npx jest --coverage --coverageReporters=text --coverageReporters=html
fi