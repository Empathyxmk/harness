#!/bin/bash
set -e

# Install main and test dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Run pytest on the tests directory with coverage report (line and branch)
coverage run --branch --source=pynubank -m pytest tests -v
coverage report
coverage html