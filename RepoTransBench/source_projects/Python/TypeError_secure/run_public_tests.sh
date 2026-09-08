#!/bin/bash
# Ensure the secure package is on PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
echo "Running public tests with pytest..."
pytest public_tests/ "$@"