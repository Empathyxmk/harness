#!/bin/bash
set -e

# Use c8 for coverage, run jest for .test.js, and node for legacy scripts
echo "Running Jest tests with coverage"
npx c8 --reporter=text --reporter=html npx jest

# Also run legacy test scripts (if required for backwards compat)
for test_file in test/test-*.js; do
  [[ "$test_file" =~ \.test\.js$ ]] && continue
  echo "Running legacy $test_file"
  node "$test_file"
done

for extra_test in test/run.js test/sample-pack.js; do
  if [ -f "$extra_test" ]; then
    echo "Running $extra_test"
    node "$extra_test"
  fi
done

echo "All tests passed!"