#!/bin/bash
set -e

# Use coverage for public tests
if [ -d public_tests ]; then
    pip install --quiet coverage
    coverage run --branch -m unittest discover -s public_tests
    coverage report --show-missing
else
    echo "No public_tests directory found!"
    exit 1
fi