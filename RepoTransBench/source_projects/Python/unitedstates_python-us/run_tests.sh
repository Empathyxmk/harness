#!/bin/bash
set -e

python3 -m pip install --upgrade pip
python3 -m pip install pytest coverage pytest-cov jellyfish

echo "Running tests with pytest and collecting coverage..."
coverage run --branch --source=us -m pytest us/tests
coverage report -m
coverage html