#!/bin/bash
set -e

# Run coverage on all tests in tests/ directory, with branch info
coverage run --branch -m unittest discover -s tests
coverage report