#!/bin/bash
set -e

# Ensure imports work
export PYTHONPATH="$(pwd):$PYTHONPATH"

pytest tests/original
pytest public_tests