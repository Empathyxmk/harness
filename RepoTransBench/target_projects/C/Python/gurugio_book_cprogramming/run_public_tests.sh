#!/bin/bash
set -e
echo "Building and running public tests..."
pytest public_tests/ -v
echo "All public tests passed!"