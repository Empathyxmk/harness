#!/bin/bash
set -e

# Run all *.public.test.mjs files using node
for testfile in *.public.test.mjs; do
  echo "Running $testfile"
  node "$testfile"
done