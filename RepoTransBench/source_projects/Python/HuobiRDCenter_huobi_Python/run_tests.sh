#!/bin/bash
set -e

# Remove broken pip install lines
# Only run tests using available tools

# Discover and run all unittests, outputting results and coverage for Python files
coverage run --branch -m unittest discover -s tests -p "test_*.py"
coverage report -m