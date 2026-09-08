#!/bin/bash
set -e

export PYTHONPATH=.

echo "Running pytest for public tests in public_tests/..."

python3 -m pytest public_tests