#!/bin/bash
# Run all public tests for the project
npx mocha public_tests/package.public.test.js
npx mocha public_tests/lib/index.public.test.js