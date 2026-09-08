#!/bin/bash
set -e

# Install dependencies
pip install pytest coverage pytest-cov

# Run coverage on tests with branch coverage and produce reports
coverage run --branch -m pytest test_contribute.py
coverage report
coverage html