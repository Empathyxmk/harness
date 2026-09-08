#!/bin/bash
# Run all public tests in public_tests directory with Jest

if [ -d public_tests ]; then
  npx jest public_tests
else
  echo "No public_tests directory found."
  exit 1
fi