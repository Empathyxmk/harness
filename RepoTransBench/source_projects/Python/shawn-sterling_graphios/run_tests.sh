#!/bin/bash
set -e

# Install dependencies if needed
pip install pytest coverage pytest-cov

echo "== Running pytest with branch+line coverage =="

coverage run --branch -m pytest tests/
coverage report --show-missing
coverage html