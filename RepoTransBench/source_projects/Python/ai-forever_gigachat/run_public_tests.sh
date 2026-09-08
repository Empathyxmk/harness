#!/bin/bash
set -e
echo "Running public tests with pytest..."
export PYTHONPATH=src
pytest public_tests/