#!/bin/bash
set -e
echo "Installing dependencies..."
npm install --no-audit --no-fund

echo "Running Jest tests with coverage..."
npx jest --coverage --coverageReporters=text --coverageReporters=html