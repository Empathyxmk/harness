#!/bin/bash
set -e

echo "Installing test dependencies..."
pip install --quiet pytest Flask Babel coverage pytest-cov pytz werkzeug

echo "Running tests with coverage and pytest..."
coverage run --branch -m pytest -v
coverage report