#!/bin/bash
# Run all public test suites

echo "Running porter.public.test.js"
npx mocha --require test/index.js "public_tests/porter.public.test.js"

echo "Running porter-branches.public.test.js"
npx mocha --require test/index.js "public_tests/porter-branches.public.test.js"