#!/bin/bash
# Install pytest only if missing and run all tests in 'tests' directory
if ! command -v pytest &> /dev/null; then
  pip install pytest
fi
pytest tests/