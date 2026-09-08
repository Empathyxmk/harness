#!/bin/bash
set -e
# Remove potential conflicting .pyc or cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -exec rm -rf {} +
coverage run --branch -m pytest tests/
coverage report --show-missing
coverage html