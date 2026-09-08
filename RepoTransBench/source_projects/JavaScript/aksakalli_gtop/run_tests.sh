#!/bin/bash
# Script to install dependencies and run all tests

set -e

npm install

# Run jest with coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html