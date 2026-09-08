#!/bin/bash
set -e

echo "Running all tests with coverage"
npm run coverage
node tests/bad.js