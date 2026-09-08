#!/bin/bash
set -e
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
pytest tests/
pytest public_tests/