#!/bin/bash
set -e

# Install requirements
pip install -r requirements.txt
pip install pytest coverage pytest-cov

# Run public tests with pytest, fail if any error
pytest public_tests/