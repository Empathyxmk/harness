#!/bin/bash
set -e

# Run all .tape.js test files using npx tape
find app -name "*.tape.js" -print0 | xargs -0 npx tape