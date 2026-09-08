#!/bin/bash
set -e
# Install minimal dependencies if needed (be idempotent, for CI robustness)
pip install pytest > /dev/null || exit 1

# Discover and run all public tests
pytest public_tests/