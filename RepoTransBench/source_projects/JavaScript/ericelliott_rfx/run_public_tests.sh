#!/bin/bash
set -e
# Discover and run all public tests in public_tests/ using tape
for testfile in public_tests/*.js; do
  echo "Running $testfile"
  node "$testfile"
done