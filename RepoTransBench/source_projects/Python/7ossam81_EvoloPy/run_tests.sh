#!/bin/bash
set -e
echo "Running tests with coverage and pytest..."
coverage run --branch -m pytest tests
coverage report --show-missing