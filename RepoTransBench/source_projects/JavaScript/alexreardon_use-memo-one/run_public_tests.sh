#!/bin/bash
set -e

# Run only public tests
npx jest --testPathPattern="public_tests/.*\\.public\\.test\\.js" --coverage=false