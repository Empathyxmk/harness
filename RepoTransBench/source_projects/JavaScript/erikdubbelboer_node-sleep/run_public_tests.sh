#!/bin/bash
set -e

npm install

# Run mocha on the public tests only
npx mocha public_tests/**/*.public.test.js

echo "All public tests passed."