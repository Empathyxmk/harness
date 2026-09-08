#!/bin/bash
# Run all public tests in the ./public_tests directory using Node's built-in test runner (tap)
if [ -d "./public_tests" ]; then
  for f in ./public_tests/*.public.test.js; do
    echo "Running $f"
    node $f
    if [ $? -ne 0 ]; then
      echo "Public test failed: $f"
      exit 1
    fi
  done
else
  echo "No public_tests directory found."
  exit 1
fi
echo "All public tests passed."