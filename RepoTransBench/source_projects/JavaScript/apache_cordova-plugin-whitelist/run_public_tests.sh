#!/bin/bash
set -e

export NODE_ENV=test

# Run all public tests using Jest, searching only in public_tests/
npx jest public_tests --testPathIgnorePatterns="node_modules"