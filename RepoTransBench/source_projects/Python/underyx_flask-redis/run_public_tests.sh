#!/bin/bash
# Run all public tests, adding project root to PYTHONPATH for imports
export PYTHONPATH=$(pwd):$PYTHONPATH
pytest public_tests