#!/bin/bash
set -e

echo "Running minimal test suite directly with node..."

# Only run our new basic assertion test files
node 02/extensions.test.js
node 05/delete.test.js
node 05/parse.test.js

echo "All minimal test files executed."