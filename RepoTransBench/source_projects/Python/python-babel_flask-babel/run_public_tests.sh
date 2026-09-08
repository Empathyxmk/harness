#!/bin/bash
set -e

echo "Installing test dependencies for public tests..."
pip install --quiet pytest Flask Babel coverage pytest-cov pytz werkzeug

echo "Running public tests with coverage and pytest..."
coverage run --branch -m pytest -v public_tests/
coverage report