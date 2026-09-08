#!/bin/bash
# Run all public tests with correct PYTHONPATH

export PYTHONPATH="$(pwd):$PYTHONPATH"
pytest public_tests/