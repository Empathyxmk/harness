#!/bin/bash
set -e

# Install main and test dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Run pytest on the public_tests directory
pytest public_tests -v