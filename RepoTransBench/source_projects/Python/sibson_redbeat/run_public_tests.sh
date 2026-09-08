#!/bin/bash
# Ensure we run with current directory as project root for proper import resolution
export PYTHONPATH=$(pwd)
pytest public_tests/