#!/bin/bash
set -e

# Assume dependencies are preinstalled or installation not possible; skip pip install
# Run all tests with coverage, including branch coverage
coverage erase
coverage run --branch -m unittest discover -s . -p "test_*.py"
coverage report
coverage html

exit $?