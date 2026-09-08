#!/bin/bash
set -e

# Run all .public.test.js test files using npx tape
find public_tests -name "*.public.test.js" -print0 | xargs -0 npx tape