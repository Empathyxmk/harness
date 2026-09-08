#!/bin/bash
set -e

pip install -r requirements/tests.txt
pip install pytest coverage pytest-cov

# Run tests with branch and line coverage for src/ dir
coverage run --branch -m pytest tests
coverage report