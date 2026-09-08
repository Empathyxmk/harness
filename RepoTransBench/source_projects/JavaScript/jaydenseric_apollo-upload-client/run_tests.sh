#!/bin/bash
set -e

# Run all .test.mjs files using node for coverage
for testfile in *.test.mjs; do
  echo "Running $testfile"
  node "$testfile"
done

if [ -f isExtractableFile.test.mjs ]; then
  echo "Running isExtractableFile.test.mjs"
  node isExtractableFile.test.mjs
fi