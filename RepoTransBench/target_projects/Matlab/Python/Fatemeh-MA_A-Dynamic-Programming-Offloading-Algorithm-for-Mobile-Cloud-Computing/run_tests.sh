#!/bin/bash
set -e

# Ensure src/ is available on PYTHONPATH for local imports
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

pytest tests/
pytest public_tests/