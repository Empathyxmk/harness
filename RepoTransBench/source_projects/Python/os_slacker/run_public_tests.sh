#!/bin/bash
set -e

# Run coverage on all public tests in public_tests/ directory, with branch info
coverage run --branch -m unittest discover -s public_tests
coverage report