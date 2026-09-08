#!/bin/bash
set -e

# Install dependencies if needed
npm install

# Run all public tests
npx jest public_tests/