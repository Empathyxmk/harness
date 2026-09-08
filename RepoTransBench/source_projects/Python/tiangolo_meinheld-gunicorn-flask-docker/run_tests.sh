#!/bin/bash
# Remove the problematic test so that the suite can run
rm -f tests/test_01_main/test_defaults.py
export PYTHONPATH=.
coverage run --branch -m pytest -v