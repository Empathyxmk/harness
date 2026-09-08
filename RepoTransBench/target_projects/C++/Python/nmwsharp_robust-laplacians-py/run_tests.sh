#!/bin/bash
set -e
export PYTHONPATH=src:$PYTHONPATH

# Run all tests in both directories
pytest tests/original/
pytest public_tests/