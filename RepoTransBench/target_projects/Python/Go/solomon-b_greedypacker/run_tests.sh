#!/bin/bash
set -e

# Only install pre-existing dependencies needed for tests to avoid PyYAML/cython issues.
pip install --upgrade pip setuptools wheel pytest coverage pytest-cov sortedcontainers

# Run all tests with coverage using pytest
coverage run --branch -m pytest
coverage report -m