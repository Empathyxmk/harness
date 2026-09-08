#!/bin/bash
# Run all public tests in the public_tests directory, making sure injector is importable
export PYTHONPATH=$(pwd):$PYTHONPATH
pytest public_tests/