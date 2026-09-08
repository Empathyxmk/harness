#!/bin/bash
set -e

echo "Running public tests..."

TESTS=$(find public_tests -name 'test_public_*.py' | tr '\n' ' ')

python3 -m pytest $TESTS