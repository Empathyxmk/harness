#!/bin/bash
# Run all public tests for the pyzbar project using the correct PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
pytest --maxfail=1 --disable-warnings public_tests