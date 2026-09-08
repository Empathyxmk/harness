#!/bin/bash
set -e

pip install pytest coverage pytest-cov pyyaml

# Run public tests and measure coverage (line and branch)
coverage run --branch -m pytest public_tests/
coverage report -m