#!/bin/bash
set -e

echo "-------------------------------------------"
echo "Running Jest PUBLIC unit tests ..."
echo "-------------------------------------------"

npx jest --testPathPattern="\.public\.test\.js$"

echo "-------------------------------------------"
echo "All public tests (if any) executed."
echo "-------------------------------------------"