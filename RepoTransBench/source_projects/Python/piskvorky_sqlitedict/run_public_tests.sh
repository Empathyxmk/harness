#!/bin/bash
# Script to run all public tests for this repository.

set -e
export PYTHONPATH=$(dirname "$0")
pytest public_tests/