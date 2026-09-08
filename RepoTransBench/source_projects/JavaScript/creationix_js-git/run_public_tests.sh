#!/bin/bash
set -e

echo "Running Jest public tests with coverage"
npx c8 --reporter=text --reporter=html npx jest public_tests/

echo "All public tests passed!"