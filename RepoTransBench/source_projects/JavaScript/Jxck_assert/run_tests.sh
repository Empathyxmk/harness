#!/bin/bash
echo "Running legacy Node tests in test/test-assert.js"
node test/test-assert.js && echo "All OK" || exit 1

echo "Running Jest tests for extended coverage"
npx jest --coverage --coverageReporters=text --coverageReporters=html