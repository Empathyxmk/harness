#!/bin/bash
# Install test dependencies, then run public tests with PYTHONPATH set to include the project root

pip install pytest
PYTHONPATH=$(pwd) pytest public_tests/