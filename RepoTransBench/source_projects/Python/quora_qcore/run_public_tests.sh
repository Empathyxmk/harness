#!/bin/bash
# Run all public tests with proper PYTHONPATH set
export PYTHONPATH=.
pytest public_tests "$@"