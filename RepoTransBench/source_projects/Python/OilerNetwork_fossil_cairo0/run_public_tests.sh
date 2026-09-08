#!/bin/bash
# Ensure all Python and pytest/unittest dependencies are satisfied for public tests
pip install -U setuptools setuptools_scm wheel pytest > /dev/null 2>&1

# Run public tests (all test_*.py files in public_tests/)
python3 -m unittest discover public_tests