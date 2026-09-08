#!/bin/bash
# Run all public tests using pytest
set -e
export PYTHONPATH=.
pytest public_tests/