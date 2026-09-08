#!/bin/bash
set -e

# Install AVA if missing (once, for CI simplicity)
if ! [ -x "$(command -v npx)" ]; then
  echo "npx is not installed." >&2
  exit 1
fi

# Run AVA tests with c8 for coverage
npx c8 --reporter=lcov --reporter=text npx ava