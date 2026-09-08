#!/bin/bash
# Ensure the src directory is in PYTHONPATH for module resolution
export PYTHONPATH="$(pwd)/src${PYTHONPATH+:$PYTHONPATH}"
pytest public_tests/