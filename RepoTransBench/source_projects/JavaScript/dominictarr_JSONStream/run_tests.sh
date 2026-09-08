#!/bin/bash
set -e

# Run all test/*.js files except known problem files:
# Exclude browser.js (browser environment), destroy_missing.js/multiple_objects.js/multiple_objects_error.js (port 9999 EADDRINUSE)
for testfile in test/*.js; do
  case "$testfile" in
    test/browser.js|test/destroy_missing.js|test/multiple_objects.js|test/multiple_objects_error.js)
      echo "Skipping $testfile (requires unavailable environment or port conflict)"
      ;;
    *)
      echo "Running $testfile"
      node "$testfile"
      ;;
  esac
done

echo "All applicable tests passed (except browser.js, destroy_missing.js, multiple_objects.js, and multiple_objects_error.js)."