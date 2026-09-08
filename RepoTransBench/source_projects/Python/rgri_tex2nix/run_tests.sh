#!/bin/bash
set -e

pip install pytest coverage pytest-cov

# Run tests with coverage (including branch coverage)
coverage run --branch -m pytest
coverage report