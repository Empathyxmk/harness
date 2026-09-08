#!/bin/bash
set -e
for file in public_tests/*.public.test.js
do
  echo "Running $file"
  node "$file"
done