#!/bin/bash
set -e
echo "Installing dependencies for public tests..."
npm install --no-audit --no-fund

echo "Running Jest public tests..."
npx jest public_tests/