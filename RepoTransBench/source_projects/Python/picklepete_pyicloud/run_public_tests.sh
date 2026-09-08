#!/bin/bash
set -e

# Install test/development dependencies
pip install -r requirements_test.txt

# Run pytest on the public_tests directory
pytest public_tests