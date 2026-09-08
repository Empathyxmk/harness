#!/bin/bash
set -e
echo "Running test/debug.test.js"
node --loader=module test/debug.test.js
echo "Running test/index.js"
node test/index.js
echo "Running test/main.js"
node test/main.js