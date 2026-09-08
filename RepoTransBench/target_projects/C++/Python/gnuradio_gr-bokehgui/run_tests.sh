#!/bin/bash
set -e
echo "===== Running ORIGINAL tests ====="
pytest tests/original/
echo
echo "===== Running PUBLIC tests ====="
pytest public_tests/