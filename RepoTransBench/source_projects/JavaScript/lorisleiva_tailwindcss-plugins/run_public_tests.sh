#!/bin/bash
set -e

# Install AVA if missing (once, for CI simplicity)
if ! [ -x "$(command -v npx)" ]; then
  echo "npx is not installed." >&2
  exit 1
fi

# Run AVA tests in public_tests/ directory
npx c8 --reporter=lcov --reporter=text npx ava "public_tests/*.public.test.js"