#!/bin/bash
# Run all existing tests with proper PYTHONPATH set
export PYTHONPATH=.
pytest qcore/tests "$@"