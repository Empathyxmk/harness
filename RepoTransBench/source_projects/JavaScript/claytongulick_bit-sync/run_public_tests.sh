#!/bin/bash
set -e
# Run only the public tests in the public_tests directory
npx jest public_tests/ --coverage=false "$@"